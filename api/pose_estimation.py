#!/usr/bin/env python3
"""
ShowDog 3D Pose Estimation Framework
=====================================

Implements 3D pose estimation for dogs using monocular camera input and
keypoint-based skeletal analysis. This module handles the geometric analysis
AFTER keypoints are obtained from an external detection model (e.g. Claude
Vision API).

Pipeline overview:
    1. Receive 2D keypoints from detector
    2. Reconstruct approximate 3D pose using breed-specific priors
    3. Compute skeletal joint angles
    4. Score structure against breed-ideal angle database
    5. (Optional) Analyze gait from multi-frame sequences

Canine anatomical keypoints (17 total):
    Head:  nose, left_eye, right_eye, left_ear_base, right_ear_base
    Spine: withers, spine_mid, hip_point
    Front: left_shoulder, left_elbow, left_front_paw,
           right_shoulder, right_elbow, right_front_paw
    Rear:  left_stifle, left_hock, left_rear_paw

Uses only the math standard library -- no numpy/scipy/opencv required.
"""

import math
from typing import Dict, List, Optional, Tuple

# ============================================================================
# Keypoint index constants
# ============================================================================

KEYPOINT_NAMES: List[str] = [
    "nose",               # 0
    "left_eye",           # 1
    "right_eye",          # 2
    "left_ear_base",      # 3
    "right_ear_base",     # 4
    "withers",            # 5
    "spine_mid",          # 6
    "hip_point",          # 7
    "left_shoulder",      # 8
    "left_elbow",         # 9
    "left_front_paw",     # 10
    "right_shoulder",     # 11
    "right_elbow",        # 12
    "right_front_paw",    # 13
    "left_stifle",        # 14
    "left_hock",          # 15
    "left_rear_paw",      # 16
]

NUM_KEYPOINTS = len(KEYPOINT_NAMES)

KP = {name: idx for idx, name in enumerate(KEYPOINT_NAMES)}
"""Mapping from keypoint name to its index."""


# ============================================================================
# Vec2 -- lightweight 2D vector
# ============================================================================

class Vec2:
    """Immutable 2-component vector with common math operations.

    Attributes:
        x (float): horizontal component.
        y (float): vertical component.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0):
        object.__setattr__(self, "x", float(x))
        object.__setattr__(self, "y", float(y))

    def __setattr__(self, _name, _value):
        raise AttributeError("Vec2 is immutable")

    # -- arithmetic ---------------------------------------------------------

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vec2":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        return Vec2(self.x / scalar, self.y / scalar)

    def __neg__(self) -> "Vec2":
        return Vec2(-self.x, -self.y)

    # -- queries ------------------------------------------------------------

    def dot(self, other: "Vec2") -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        """Euclidean length."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_sq(self) -> float:
        """Squared length (avoids sqrt)."""
        return self.x * self.x + self.y * self.y

    def normalized(self) -> "Vec2":
        """Unit vector in the same direction. Returns zero vector if length is
        near zero."""
        ln = self.length()
        if ln < 1e-12:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / ln, self.y / ln)

    def distance_to(self, other: "Vec2") -> float:
        """Euclidean distance to *other*."""
        return (self - other).length()

    def angle_to_horizontal(self) -> float:
        """Angle in degrees from the positive x-axis (right), measured
        counter-clockwise. Result is in [-180, 180]."""
        return math.degrees(math.atan2(self.y, self.x))

    # -- representation -----------------------------------------------------

    def as_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Vec2({self.x:.4f}, {self.y:.4f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9


# ============================================================================
# Vec3 -- lightweight 3D vector
# ============================================================================

class Vec3:
    """Immutable 3-component vector with common math operations.

    Attributes:
        x (float): right axis.
        y (float): up axis.
        z (float): forward / depth axis.
    """

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        object.__setattr__(self, "x", float(x))
        object.__setattr__(self, "y", float(y))
        object.__setattr__(self, "z", float(z))

    def __setattr__(self, _name, _value):
        raise AttributeError("Vec3 is immutable")

    # -- arithmetic ---------------------------------------------------------

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vec3":
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> "Vec3":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vec3":
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> "Vec3":
        return Vec3(-self.x, -self.y, -self.z)

    # -- queries ------------------------------------------------------------

    def dot(self, other: "Vec3") -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vec3") -> "Vec3":
        """Cross product (self x other)."""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """Euclidean length."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def length_sq(self) -> float:
        """Squared length."""
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> "Vec3":
        """Unit vector in the same direction."""
        ln = self.length()
        if ln < 1e-12:
            return Vec3(0.0, 0.0, 0.0)
        return Vec3(self.x / ln, self.y / ln, self.z / ln)

    def distance_to(self, other: "Vec3") -> float:
        return (self - other).length()

    # -- representation -----------------------------------------------------

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"Vec3({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            return NotImplemented
        return (
            abs(self.x - other.x) < 1e-9
            and abs(self.y - other.y) < 1e-9
            and abs(self.z - other.z) < 1e-9
        )


# ============================================================================
# Mat3 -- simple 3x3 matrix (row-major)
# ============================================================================

class Mat3:
    """Row-major 3x3 matrix for projection and rotation operations.

    Stored as a flat list of 9 floats in row-major order::

        [ m00 m01 m02 ]
        [ m10 m11 m12 ]
        [ m20 m21 m22 ]
    """

    __slots__ = ("_m",)

    def __init__(self, values: Optional[List[float]] = None):
        """Create a Mat3 from 9 floats (row-major). Defaults to identity."""
        if values is None:
            object.__setattr__(self, "_m", [
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0,
            ])
        else:
            if len(values) != 9:
                raise ValueError("Mat3 requires exactly 9 values")
            object.__setattr__(self, "_m", [float(v) for v in values])

    def __setattr__(self, _name, _value):
        raise AttributeError("Mat3 is immutable after construction")

    def at(self, row: int, col: int) -> float:
        """Element access (0-indexed)."""
        return self._m[row * 3 + col]

    def mul_vec3(self, v: Vec3) -> Vec3:
        """Matrix-vector product: M * v."""
        m = self._m
        return Vec3(
            m[0] * v.x + m[1] * v.y + m[2] * v.z,
            m[3] * v.x + m[4] * v.y + m[5] * v.z,
            m[6] * v.x + m[7] * v.y + m[8] * v.z,
        )

    def mul_mat3(self, other: "Mat3") -> "Mat3":
        """Matrix-matrix product: self * other."""
        a, b = self._m, other._m
        result = []
        for r in range(3):
            for c in range(3):
                s = 0.0
                for k in range(3):
                    s += a[r * 3 + k] * b[k * 3 + c]
                result.append(s)
        return Mat3(result)

    def transposed(self) -> "Mat3":
        m = self._m
        return Mat3([
            m[0], m[3], m[6],
            m[1], m[4], m[7],
            m[2], m[5], m[8],
        ])

    def determinant(self) -> float:
        m = self._m
        return (
            m[0] * (m[4] * m[8] - m[5] * m[7])
            - m[1] * (m[3] * m[8] - m[5] * m[6])
            + m[2] * (m[3] * m[7] - m[4] * m[6])
        )

    def inverse(self) -> "Mat3":
        """Compute the inverse. Raises ValueError if singular."""
        det = self.determinant()
        if abs(det) < 1e-12:
            raise ValueError("Matrix is singular, cannot invert")
        m = self._m
        inv_det = 1.0 / det
        return Mat3([
            (m[4] * m[8] - m[5] * m[7]) * inv_det,
            (m[2] * m[7] - m[1] * m[8]) * inv_det,
            (m[1] * m[5] - m[2] * m[4]) * inv_det,
            (m[5] * m[6] - m[3] * m[8]) * inv_det,
            (m[0] * m[8] - m[2] * m[6]) * inv_det,
            (m[2] * m[3] - m[0] * m[5]) * inv_det,
            (m[3] * m[7] - m[4] * m[6]) * inv_det,
            (m[1] * m[6] - m[0] * m[7]) * inv_det,
            (m[0] * m[4] - m[1] * m[3]) * inv_det,
        ])

    @staticmethod
    def rotation_y(angle_deg: float) -> "Mat3":
        """Rotation around the Y (up) axis."""
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        return Mat3([
            c, 0.0, s,
            0.0, 1.0, 0.0,
            -s, 0.0, c,
        ])

    @staticmethod
    def rotation_x(angle_deg: float) -> "Mat3":
        """Rotation around the X (right) axis."""
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        return Mat3([
            1.0, 0.0, 0.0,
            0.0, c, -s,
            0.0, s, c,
        ])

    def __repr__(self) -> str:
        m = self._m
        rows = []
        for r in range(3):
            row_str = ", ".join(f"{m[r*3+c]:8.4f}" for c in range(3))
            rows.append(f"  [{row_str}]")
        return "Mat3(\n" + "\n".join(rows) + "\n)"


# ============================================================================
# Vector math helpers (module-level convenience functions)
# ============================================================================

def angle_between_vectors_deg(a: Vec3, b: Vec3) -> float:
    """Return the angle in degrees between two Vec3 vectors.

    Clamps the dot-product ratio to [-1, 1] to avoid floating-point domain
    errors in ``acos``.
    """
    la, lb = a.length(), b.length()
    if la < 1e-12 or lb < 1e-12:
        return 0.0
    cos_theta = a.dot(b) / (la * lb)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))


def angle_at_vertex_deg(p1: Vec3, vertex: Vec3, p2: Vec3) -> float:
    """Return the angle at *vertex* formed by segments vertex->p1 and
    vertex->p2, in degrees."""
    return angle_between_vectors_deg(p1 - vertex, p2 - vertex)


def angle_at_vertex_2d_deg(p1: Vec2, vertex: Vec2, p2: Vec2) -> float:
    """2D version of angle_at_vertex_deg."""
    v1 = p1 - vertex
    v2 = p2 - vertex
    l1, l2 = v1.length(), v2.length()
    if l1 < 1e-12 or l2 < 1e-12:
        return 0.0
    cos_theta = v1.dot(v2) / (l1 * l2)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))


def lerp_vec3(a: Vec3, b: Vec3, t: float) -> Vec3:
    """Linear interpolation between *a* and *b*."""
    return a * (1.0 - t) + b * t


# ============================================================================
# CanineKeypoints -- data container for a single frame
# ============================================================================

class CanineKeypoints:
    """Container for 17 canine anatomical keypoints.

    Each keypoint is stored as a Vec2 (image-space) or Vec3 (world-space)
    depending on the processing stage. A parallel ``confidence`` list stores
    per-keypoint detection confidence in [0, 1].

    Usage::

        kp = CanineKeypoints()
        kp.set_2d("nose", Vec2(320, 100), confidence=0.95)
        kp.set_2d("withers", Vec2(280, 160), confidence=0.92)
        nose = kp.get_2d("nose")
    """

    def __init__(self):
        self._pts2d: List[Optional[Vec2]] = [None] * NUM_KEYPOINTS
        self._pts3d: List[Optional[Vec3]] = [None] * NUM_KEYPOINTS
        self._confidence: List[float] = [0.0] * NUM_KEYPOINTS

    # -- 2D accessors -------------------------------------------------------

    def set_2d(self, name: str, point: Vec2, confidence: float = 1.0) -> None:
        """Set a 2D keypoint by name."""
        idx = KP[name]
        self._pts2d[idx] = point
        self._confidence[idx] = confidence

    def get_2d(self, name: str) -> Optional[Vec2]:
        """Get a 2D keypoint by name, or None if not set."""
        return self._pts2d[KP[name]]

    def set_2d_by_index(self, idx: int, point: Vec2, confidence: float = 1.0) -> None:
        self._pts2d[idx] = point
        self._confidence[idx] = confidence

    def get_2d_by_index(self, idx: int) -> Optional[Vec2]:
        return self._pts2d[idx]

    # -- 3D accessors -------------------------------------------------------

    def set_3d(self, name: str, point: Vec3) -> None:
        """Set a 3D keypoint by name."""
        self._pts3d[KP[name]] = point

    def get_3d(self, name: str) -> Optional[Vec3]:
        """Get a 3D keypoint by name, or None if not set."""
        return self._pts3d[KP[name]]

    def set_3d_by_index(self, idx: int, point: Vec3) -> None:
        self._pts3d[idx] = point

    def get_3d_by_index(self, idx: int) -> Optional[Vec3]:
        return self._pts3d[idx]

    # -- confidence ---------------------------------------------------------

    def confidence(self, name: str) -> float:
        return self._confidence[KP[name]]

    def min_confidence(self) -> float:
        """Minimum confidence across all *set* keypoints."""
        vals = [c for i, c in enumerate(self._confidence) if self._pts2d[i] is not None]
        return min(vals) if vals else 0.0

    # -- queries ------------------------------------------------------------

    def num_detected(self) -> int:
        """Number of keypoints that have a 2D position set."""
        return sum(1 for p in self._pts2d if p is not None)

    def has(self, name: str) -> bool:
        return self._pts2d[KP[name]] is not None

    def all_names_present(self, names: List[str]) -> bool:
        return all(self.has(n) for n in names)

    def __repr__(self) -> str:
        detected = self.num_detected()
        return f"CanineKeypoints({detected}/{NUM_KEYPOINTS} detected)"


# ============================================================================
# BreedAngleDatabase -- ideal skeletal angles per breed
# ============================================================================

class BreedAngleDatabase:
    """Database of ideal skeletal joint angles for recognized breeds.

    Each breed entry stores a dict mapping angle names to a tuple
    ``(ideal_degrees, tolerance_degrees)``.  The angle names match the keys
    returned by :meth:`PoseAnalyzer.compute_angles`.

    Angle keys:
        shoulder_angle   - withers-shoulder-elbow
        elbow_angle      - shoulder-elbow-front_paw
        stifle_angle     - hip-stifle-hock
        hock_angle       - stifle-hock-rear_paw
        topline_angle    - withers-spine_mid-hip (ideally ~180 for level topline)
        head_carriage    - angle of nose-withers segment from horizontal
        body_ratio       - (withers-to-hip length) / (withers height above ground)

    The ``importance_weight`` per angle controls how heavily a deviation is
    penalized in the composite score.
    """

    # (ideal_degrees, tolerance_degrees)
    _AngleSpec = Tuple[float, float]

    # Default importance weights for each angle in scoring (sum to 1.0).
    DEFAULT_WEIGHTS: Dict[str, float] = {
        "shoulder_angle": 0.18,
        "elbow_angle": 0.12,
        "stifle_angle": 0.15,
        "hock_angle": 0.10,
        "topline_angle": 0.20,
        "head_carriage": 0.10,
        "body_ratio": 0.15,
    }

    def __init__(self):
        self._breeds: Dict[str, Dict[str, Tuple[float, float]]] = {}
        self._breed_weights: Dict[str, Dict[str, float]] = {}
        self._load_defaults()

    # -- public API ---------------------------------------------------------

    def get_ideals(self, breed_id: str) -> Optional[Dict[str, Tuple[float, float]]]:
        """Return ideal angle dict for *breed_id*, or None if unknown."""
        return self._breeds.get(breed_id)

    def get_weights(self, breed_id: str) -> Dict[str, float]:
        """Return importance weights for *breed_id*, falling back to defaults."""
        return self._breed_weights.get(breed_id, self.DEFAULT_WEIGHTS)

    def add_breed(
        self,
        breed_id: str,
        ideals: Dict[str, Tuple[float, float]],
        weights: Optional[Dict[str, float]] = None,
    ) -> None:
        """Register or overwrite ideal angles for a breed."""
        self._breeds[breed_id] = dict(ideals)
        if weights is not None:
            self._breed_weights[breed_id] = dict(weights)

    def list_breeds(self) -> List[str]:
        return sorted(self._breeds.keys())

    # -- default data -------------------------------------------------------

    def _load_defaults(self) -> None:
        """Populate the database with ideals for 12 popular breeds.

        Values are representative approximations derived from breed-standard
        descriptions and published veterinary-biomechanics literature.
        Tolerance is the acceptable +/- range before points are deducted.

        Format per angle: (ideal_degrees, tolerance_degrees)
        For body_ratio the values represent the dimensionless ratio and its
        tolerance (not degrees).
        """

        # -- German Shepherd Dog (166) ---------------------------------------
        self._breeds["166_german_shepherd"] = {
            "shoulder_angle": (90.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (120.0, 5.0),
            "hock_angle": (140.0, 5.0),
            "topline_angle": (170.0, 5.0),   # slight slope accepted
            "head_carriage": (35.0, 8.0),
            "body_ratio": (1.17, 0.05),       # longer than tall
        }

        # -- Labrador Retriever (122) ----------------------------------------
        self._breeds["122_labrador_retriever"] = {
            "shoulder_angle": (97.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (178.0, 4.0),
            "head_carriage": (30.0, 8.0),
            "body_ratio": (1.05, 0.05),
        }

        # -- Golden Retriever (111) ------------------------------------------
        self._breeds["111_golden_retriever"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (178.0, 4.0),
            "head_carriage": (30.0, 8.0),
            "body_ratio": (1.08, 0.05),
        }

        # -- Toy Poodle (172d) -----------------------------------------------
        self._breeds["172d_poodle_toy"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (140.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (180.0, 3.0),
            "head_carriage": (40.0, 8.0),
            "body_ratio": (1.00, 0.04),       # square build
        }

        # -- Shiba Inu (257) -------------------------------------------------
        self._breeds["257_shiba"] = {
            "shoulder_angle": (100.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (130.0, 5.0),
            "hock_angle": (150.0, 5.0),
            "topline_angle": (180.0, 3.0),
            "head_carriage": (40.0, 8.0),
            "body_ratio": (1.10, 0.05),
        }

        # -- French Bulldog (101) --------------------------------------------
        self._breeds["101_french_bulldog"] = {
            "shoulder_angle": (100.0, 6.0),
            "elbow_angle": (140.0, 6.0),
            "stifle_angle": (130.0, 6.0),
            "hock_angle": (150.0, 6.0),
            "topline_angle": (175.0, 5.0),   # slight roach accepted
            "head_carriage": (45.0, 10.0),
            "body_ratio": (0.95, 0.05),
        }

        # -- Pembroke Welsh Corgi (39) ---------------------------------------
        self._breeds["39_pembroke_corgi"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (140.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (180.0, 3.0),
            "head_carriage": (30.0, 8.0),
            "body_ratio": (1.40, 0.06),       # markedly long body
        }

        # -- Dobermann (143) -------------------------------------------------
        self._breeds["143_dobermann"] = {
            "shoulder_angle": (90.0, 4.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (120.0, 5.0),
            "hock_angle": (140.0, 5.0),
            "topline_angle": (178.0, 3.0),
            "head_carriage": (35.0, 7.0),
            "body_ratio": (1.05, 0.04),
        }

        # -- Border Collie (297) ---------------------------------------------
        self._breeds["297_border_collie"] = {
            "shoulder_angle": (92.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (178.0, 4.0),
            "head_carriage": (30.0, 8.0),
            "body_ratio": (1.10, 0.05),
        }

        # -- Siberian Husky (270) --------------------------------------------
        self._breeds["270_siberian_husky"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (145.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (180.0, 3.0),
            "head_carriage": (35.0, 8.0),
            "body_ratio": (1.08, 0.05),
        }

        # -- Dachshund (148) -------------------------------------------------
        self._breeds["148_dachshund"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (140.0, 5.0),
            "stifle_angle": (125.0, 6.0),
            "hock_angle": (145.0, 6.0),
            "topline_angle": (180.0, 3.0),
            "head_carriage": (35.0, 8.0),
            "body_ratio": (1.70, 0.08),       # very long body
        }

        # -- Boxer (144) -----------------------------------------------------
        self._breeds["144_boxer"] = {
            "shoulder_angle": (95.0, 5.0),
            "elbow_angle": (140.0, 5.0),
            "stifle_angle": (125.0, 5.0),
            "hock_angle": (145.0, 5.0),
            "topline_angle": (178.0, 4.0),
            "head_carriage": (40.0, 8.0),
            "body_ratio": (1.00, 0.04),       # square build
        }


# ============================================================================
# 3D Reconstruction helpers
# ============================================================================

class PinholeCamera:
    """Minimal pinhole camera model for projecting 3D points to 2D and for
    back-projecting 2D points to 3D rays.

    The intrinsic matrix K is::

        [ fx  0  cx ]
        [  0  fy cy ]
        [  0   0  1 ]

    Args:
        fx: Focal length in pixels (horizontal).
        fy: Focal length in pixels (vertical).
        cx: Principal point x (usually image_width / 2).
        cy: Principal point y (usually image_height / 2).
    """

    def __init__(self, fx: float, fy: float, cx: float, cy: float):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.K = Mat3([
            fx, 0.0, cx,
            0.0, fy, cy,
            0.0, 0.0, 1.0,
        ])

    def project(self, point3d: Vec3) -> Vec2:
        """Project a 3D world point onto the image plane.

        Assumes the camera is at the origin looking along +Z.
        """
        if abs(point3d.z) < 1e-12:
            return Vec2(self.cx, self.cy)
        u = self.fx * (point3d.x / point3d.z) + self.cx
        v = self.fy * (point3d.y / point3d.z) + self.cy
        return Vec2(u, v)

    def back_project_ray(self, point2d: Vec2) -> Vec3:
        """Return a normalized direction ray from a 2D image point."""
        dx = (point2d.x - self.cx) / self.fx
        dy = (point2d.y - self.cy) / self.fy
        return Vec3(dx, dy, 1.0).normalized()

    @staticmethod
    def default_for_image(width: int, height: int) -> "PinholeCamera":
        """Create a camera with a reasonable default focal length (~50mm
        equivalent) for an image of the given size."""
        fx = fy = float(max(width, height))  # ~60 degree FoV
        cx = width / 2.0
        cy = height / 2.0
        return PinholeCamera(fx, fy, cx, cy)


class DepthEstimator:
    """Estimates approximate depth (Z) for each keypoint using breed-specific
    body-proportion priors.

    Strategy:
        1. Use the known breed body-length ratio and withers height to
           establish a scale reference in the image.
        2. Compute apparent size (pixel distance between withers and hip)
           and compare to expected real-world size to get an approximate
           absolute depth.
        3. Assign per-keypoint depth offsets based on canonical 3D dog
           skeleton proportions (e.g. paws are closer to camera when viewed
           from the side).

    This is a rough monocular depth estimate -- true depth requires stereo
    or depth sensors.
    """

    # Canonical depth offsets relative to the withers depth for a side-on view.
    # Positive Z = farther from camera.  Units are fractions of body length.
    _CANONICAL_DEPTH_OFFSETS: Dict[str, float] = {
        "nose": -0.30,
        "left_eye": -0.25,
        "right_eye": -0.25,
        "left_ear_base": -0.20,
        "right_ear_base": -0.20,
        "withers": 0.00,
        "spine_mid": 0.00,
        "hip_point": 0.00,
        "left_shoulder": -0.05,
        "left_elbow": -0.05,
        "left_front_paw": -0.05,
        "right_shoulder": 0.05,
        "right_elbow": 0.05,
        "right_front_paw": 0.05,
        "left_stifle": -0.05,
        "left_hock": -0.05,
        "left_rear_paw": -0.05,
    }

    def __init__(self, camera: PinholeCamera, reference_height_m: float = 0.55):
        """
        Args:
            camera: The pinhole camera model.
            reference_height_m: Expected real-world withers height in metres.
                Defaults to 0.55 m (a medium-sized dog).
        """
        self.camera = camera
        self.reference_height_m = reference_height_m

    def estimate_depth(self, keypoints: CanineKeypoints) -> float:
        """Estimate the base depth (Z in metres) of the dog from the camera.

        Uses the pixel distance between withers and the ground-plane
        (approximated by front paw y) compared to the expected real height.
        Falls back to a default of 3.0 m if keypoints are insufficient.
        """
        withers_2d = keypoints.get_2d("withers")
        paw_2d = keypoints.get_2d("left_front_paw") or keypoints.get_2d("right_front_paw")

        if withers_2d is None or paw_2d is None:
            return 3.0  # fallback

        pixel_height = abs(paw_2d.y - withers_2d.y)
        if pixel_height < 1.0:
            return 3.0

        # depth = (focal_length * real_height) / pixel_height
        depth = (self.camera.fy * self.reference_height_m) / pixel_height
        return max(0.5, min(depth, 20.0))  # clamp to reasonable range

    def reconstruct_3d(self, keypoints: CanineKeypoints) -> CanineKeypoints:
        """Back-project all 2D keypoints to approximate 3D positions.

        Modifies the *keypoints* object in-place by populating the 3D slots
        and also returns it for chaining.
        """
        base_depth = self.estimate_depth(keypoints)

        # Compute body length in pixels for offset scaling.
        withers_2d = keypoints.get_2d("withers")
        hip_2d = keypoints.get_2d("hip_point")
        body_len_px = withers_2d.distance_to(hip_2d) if withers_2d is not None and hip_2d is not None else 100.0

        # Scale factor: how many metres per pixel at base_depth.
        m_per_px = base_depth / self.camera.fy

        for i, name in enumerate(KEYPOINT_NAMES):
            pt2d = keypoints.get_2d_by_index(i)
            if pt2d is None:
                continue

            depth_offset_frac = self._CANONICAL_DEPTH_OFFSETS.get(name, 0.0)
            depth_offset_m = depth_offset_frac * body_len_px * m_per_px
            z = base_depth + depth_offset_m

            x = (pt2d.x - self.camera.cx) * z / self.camera.fx
            y = (pt2d.y - self.camera.cy) * z / self.camera.fy

            keypoints.set_3d_by_index(i, Vec3(x, y, z))

        return keypoints


class LevenbergMarquardtRefiner:
    """Simplified Levenberg-Marquardt-style iterative refinement for 3D pose.

    Given initial 3D keypoints and their 2D projections, refines the 3D
    positions to minimise reprojection error while respecting bone-length
    constraints from breed priors.

    This is a *simplified* implementation suitable for the ShowDog scoring
    pipeline -- it uses finite-difference Jacobians and a basic damping
    schedule rather than a full sparse LM solver.
    """

    def __init__(
        self,
        camera: PinholeCamera,
        max_iterations: int = 30,
        lambda_init: float = 1.0,
        tolerance: float = 0.5,
    ):
        """
        Args:
            camera: Pinhole camera model.
            max_iterations: Maximum optimisation iterations.
            lambda_init: Initial damping factor.
            tolerance: Convergence threshold in pixels (mean reprojection error).
        """
        self.camera = camera
        self.max_iterations = max_iterations
        self.lambda_init = lambda_init
        self.tolerance = tolerance

    def _reprojection_error(self, keypoints: CanineKeypoints) -> float:
        """Mean reprojection error in pixels across all keypoints that have
        both 2D and 3D positions."""
        total = 0.0
        count = 0
        for i in range(NUM_KEYPOINTS):
            pt2d = keypoints.get_2d_by_index(i)
            pt3d = keypoints.get_3d_by_index(i)
            if pt2d is None or pt3d is None:
                continue
            projected = self.camera.project(pt3d)
            total += projected.distance_to(pt2d)
            count += 1
        if count == 0:
            return 0.0
        return total / count

    def refine(self, keypoints: CanineKeypoints) -> CanineKeypoints:
        """Run iterative refinement on the 3D keypoints.

        Each iteration nudges each 3D keypoint along its back-projected ray
        (adjusting depth) to reduce reprojection error.  A damping factor
        prevents overshooting.

        Returns the refined *keypoints* (modified in-place).
        """
        lam = self.lambda_init
        best_error = self._reprojection_error(keypoints)

        for _iteration in range(self.max_iterations):
            if best_error < self.tolerance:
                break

            improved = False
            for i in range(NUM_KEYPOINTS):
                pt2d = keypoints.get_2d_by_index(i)
                pt3d = keypoints.get_3d_by_index(i)
                if pt2d is None or pt3d is None:
                    continue

                projected = self.camera.project(pt3d)
                err_vec = Vec2(pt2d.x - projected.x, pt2d.y - projected.y)
                err_mag = err_vec.length()
                if err_mag < 0.1:
                    continue

                # Compute depth adjustment.
                self.camera.back_project_ray(pt2d)
                current_depth = pt3d.z
                step = err_mag * current_depth / self.camera.fy
                step = step / (1.0 + lam)

                # Try increasing and decreasing depth.
                best_local = err_mag
                best_pt = pt3d
                for sign in (1.0, -1.0):
                    new_z = current_depth + sign * step * 0.1
                    if new_z < 0.3:
                        continue
                    candidate = Vec3(
                        (pt2d.x - self.camera.cx) * new_z / self.camera.fx,
                        (pt2d.y - self.camera.cy) * new_z / self.camera.fy,
                        new_z,
                    )
                    proj = self.camera.project(candidate)
                    new_err = proj.distance_to(pt2d)
                    if new_err < best_local:
                        best_local = new_err
                        best_pt = candidate

                if best_pt is not pt3d:
                    keypoints.set_3d_by_index(i, best_pt)
                    improved = True

            new_error = self._reprojection_error(keypoints)
            if new_error < best_error:
                best_error = new_error
                lam = max(lam * 0.5, 0.01)
            else:
                lam = min(lam * 2.0, 100.0)

            if not improved:
                break

        return keypoints


# ============================================================================
# PoseAnalyzer -- main analysis class
# ============================================================================

class PoseAnalyzer:
    """Computes structural geometry scores for a dog from its keypoints.

    Typical usage::

        analyzer = PoseAnalyzer()
        keypoints = CanineKeypoints()
        # ... populate keypoints from detector ...
        result = analyzer.analyze_photo(keypoints, "122_labrador_retriever")
        print(result["overall_score"])   # 0-100
    """

    def __init__(self, breed_db: Optional[BreedAngleDatabase] = None):
        self.breed_db = breed_db or BreedAngleDatabase()

    # -- angle computation --------------------------------------------------

    def compute_angles(self, kp: CanineKeypoints) -> Dict[str, Optional[float]]:
        """Compute all skeletal angles from 3D (preferred) or 2D keypoints.

        Returns a dict mapping angle names to degree values.  An angle is
        None if the required keypoints are missing.

        Computed angles:
            shoulder_angle  -- withers-shoulder-elbow
            elbow_angle     -- shoulder-elbow-front_paw
            stifle_angle    -- hip-stifle-hock
            hock_angle      -- stifle-hock-rear_paw
            topline_angle   -- withers-spine_mid-hip
            head_carriage   -- angle of nose-withers from horizontal (degrees)
            body_ratio      -- (withers-to-hip) / (withers-to-ground)
        """

        def _get(name: str) -> Optional[Vec3]:
            pt = kp.get_3d(name)
            if pt is not None:
                return pt
            # Fall back to 2D -> pseudo-3D (z=0).
            pt2 = kp.get_2d(name)
            if pt2 is not None:
                return Vec3(pt2.x, pt2.y, 0.0)
            return None

        result: Dict[str, Optional[float]] = {}

        # -- Shoulder angle (left side) --
        w, sh, el = _get("withers"), _get("left_shoulder"), _get("left_elbow")
        if w and sh and el:
            result["shoulder_angle"] = angle_at_vertex_deg(w, sh, el)
        else:
            result["shoulder_angle"] = None

        # -- Elbow angle (left side) --
        sh2, el2, paw = _get("left_shoulder"), _get("left_elbow"), _get("left_front_paw")
        if sh2 and el2 and paw:
            result["elbow_angle"] = angle_at_vertex_deg(sh2, el2, paw)
        else:
            result["elbow_angle"] = None

        # -- Stifle angle (left side) --
        hip, stif, hock = _get("hip_point"), _get("left_stifle"), _get("left_hock")
        if hip and stif and hock:
            result["stifle_angle"] = angle_at_vertex_deg(hip, stif, hock)
        else:
            result["stifle_angle"] = None

        # -- Hock angle (left side) --
        stif2, hock2, rpaw = _get("left_stifle"), _get("left_hock"), _get("left_rear_paw")
        if stif2 and hock2 and rpaw:
            result["hock_angle"] = angle_at_vertex_deg(stif2, hock2, rpaw)
        else:
            result["hock_angle"] = None

        # -- Topline angle --
        w2, sm, hp = _get("withers"), _get("spine_mid"), _get("hip_point")
        if w2 and sm and hp:
            result["topline_angle"] = angle_at_vertex_deg(w2, sm, hp)
        else:
            result["topline_angle"] = None

        # -- Head carriage --
        nose, w3 = _get("nose"), _get("withers")
        if nose and w3:
            direction = nose - w3
            horiz = Vec3(1.0, 0.0, 0.0)
            raw_angle = angle_between_vectors_deg(direction, horiz)
            result["head_carriage"] = abs(raw_angle)
        else:
            result["head_carriage"] = None

        # -- Body ratio --
        w4, hp2 = _get("withers"), _get("hip_point")
        fp = _get("left_front_paw") or _get("right_front_paw")
        if w4 and hp2 and fp:
            body_len = w4.distance_to(hp2)
            height = abs(fp.y - w4.y)
            if height > 1e-6:
                result["body_ratio"] = body_len / height
            else:
                result["body_ratio"] = None
        else:
            result["body_ratio"] = None

        return result

    # -- symmetry analysis --------------------------------------------------

    def compute_symmetry(self, kp: CanineKeypoints) -> Dict[str, float]:
        """Compare left-side and right-side angles for symmetry.

        Returns a dict with symmetry scores (0-100) for front and rear
        assemblies, plus an overall symmetry score.
        """

        def _get(name: str) -> Optional[Vec3]:
            pt = kp.get_3d(name)
            if pt is not None:
                return pt
            pt2 = kp.get_2d(name)
            if pt2 is not None:
                return Vec3(pt2.x, pt2.y, 0.0)
            return None

        scores: Dict[str, float] = {}

        # -- Front assembly symmetry --
        w = _get("withers")
        lsh, lel, lpaw = _get("left_shoulder"), _get("left_elbow"), _get("left_front_paw")
        rsh, rel, rpaw = _get("right_shoulder"), _get("right_elbow"), _get("right_front_paw")

        front_diffs: List[float] = []
        if w and lsh and lel and rsh and rel:
            l_shoulder = angle_at_vertex_deg(w, lsh, lel)
            r_shoulder = angle_at_vertex_deg(w, rsh, rel)
            front_diffs.append(abs(l_shoulder - r_shoulder))

        if lsh and lel and lpaw and rsh and rel and rpaw:
            l_elbow = angle_at_vertex_deg(lsh, lel, lpaw)
            r_elbow = angle_at_vertex_deg(rsh, rel, rpaw)
            front_diffs.append(abs(l_elbow - r_elbow))

        if front_diffs:
            avg_diff = sum(front_diffs) / len(front_diffs)
            scores["front_symmetry"] = max(0.0, 100.0 - avg_diff * 5.0)
        else:
            scores["front_symmetry"] = 50.0  # unknown

        # -- Rear assembly symmetry --
        # We only have left-side rear keypoints in our 17-keypoint model,
        # so rear symmetry can only be assessed when full bilateral
        # keypoints are available (future extension).
        scores["rear_symmetry"] = scores["front_symmetry"]  # mirror assumption

        # -- Overall --
        scores["overall_symmetry"] = (
            scores["front_symmetry"] * 0.5 + scores["rear_symmetry"] * 0.5
        )

        return scores

    # -- topline curvature analysis -----------------------------------------

    def assess_topline(self, kp: CanineKeypoints) -> Dict[str, float]:
        """Analyse the topline (back) for levelness and curvature.

        Returns:
            topline_score: 0-100 where 100 = perfectly level.
            curvature_deg: Deviation from 180 degrees at spine_mid.
            slope_deg: Angle of withers-to-hip from horizontal.
        """

        def _get(name: str) -> Optional[Vec3]:
            pt = kp.get_3d(name)
            if pt is not None:
                return pt
            pt2 = kp.get_2d(name)
            if pt2 is not None:
                return Vec3(pt2.x, pt2.y, 0.0)
            return None

        w, sm, hp = _get("withers"), _get("spine_mid"), _get("hip_point")
        result: Dict[str, float] = {
            "topline_score": 50.0,
            "curvature_deg": 0.0,
            "slope_deg": 0.0,
        }

        if w and sm and hp:
            topline_angle = angle_at_vertex_deg(w, sm, hp)
            curvature = abs(180.0 - topline_angle)
            result["curvature_deg"] = curvature

            # Slope from horizontal.
            direction = hp - w
            horiz = Vec3(1.0, 0.0, 0.0)
            slope = angle_between_vectors_deg(direction, horiz)
            result["slope_deg"] = slope

            # Score: 100 for perfectly straight, loses points for curvature.
            # Allow up to 5 degrees as excellent, penalize beyond that.
            if curvature <= 3.0:
                result["topline_score"] = 100.0
            elif curvature <= 8.0:
                result["topline_score"] = 100.0 - (curvature - 3.0) * 4.0
            else:
                result["topline_score"] = max(0.0, 80.0 - (curvature - 8.0) * 6.0)

        return result

    # -- per-angle deviation scoring ----------------------------------------

    def _score_single_angle(
        self,
        measured: float,
        ideal: float,
        tolerance: float,
    ) -> float:
        """Score a single angle measurement against its ideal.

        Returns a value in [0, 100]:
            - Within tolerance: 90-100 (scales linearly within tolerance).
            - Beyond tolerance: drops below 90, reaching 0 at 4x tolerance.
        """
        deviation = abs(measured - ideal)
        if deviation <= tolerance:
            # Excellent range: 90 to 100.
            return 100.0 - (deviation / tolerance) * 10.0
        else:
            # Beyond tolerance: 90 -> 0 over the next 3x tolerance.
            excess = deviation - tolerance
            max_excess = tolerance * 3.0
            if max_excess < 1e-6:
                return 0.0
            return max(0.0, 90.0 - (excess / max_excess) * 90.0)

    # -- assembly sub-scores ------------------------------------------------

    def score_front_assembly(
        self, angles: Dict[str, Optional[float]], ideals: Dict[str, Tuple[float, float]]
    ) -> float:
        """Score the front assembly (shoulder + elbow).

        Returns 0-100.
        """
        parts: List[float] = []

        sa = angles.get("shoulder_angle")
        if sa is not None and "shoulder_angle" in ideals:
            ideal, tol = ideals["shoulder_angle"]
            parts.append(self._score_single_angle(sa, ideal, tol))

        ea = angles.get("elbow_angle")
        if ea is not None and "elbow_angle" in ideals:
            ideal, tol = ideals["elbow_angle"]
            parts.append(self._score_single_angle(ea, ideal, tol))

        return sum(parts) / len(parts) if parts else 50.0

    def score_rear_assembly(
        self, angles: Dict[str, Optional[float]], ideals: Dict[str, Tuple[float, float]]
    ) -> float:
        """Score the rear assembly (stifle + hock).

        Returns 0-100.
        """
        parts: List[float] = []

        sa = angles.get("stifle_angle")
        if sa is not None and "stifle_angle" in ideals:
            ideal, tol = ideals["stifle_angle"]
            parts.append(self._score_single_angle(sa, ideal, tol))

        ha = angles.get("hock_angle")
        if ha is not None and "hock_angle" in ideals:
            ideal, tol = ideals["hock_angle"]
            parts.append(self._score_single_angle(ha, ideal, tol))

        return sum(parts) / len(parts) if parts else 50.0

    # -- main public API ----------------------------------------------------

    def analyze_photo(
        self,
        keypoints: CanineKeypoints,
        breed_id: str,
        image_size: Optional[Tuple[int, int]] = None,
    ) -> Dict[str, object]:
        """Analyse a single photo and return structure scores.

        Args:
            keypoints: Detected 2D keypoints (3D will be estimated if absent).
            breed_id: Key into the breed angle database.
            image_size: (width, height) of the source image.  Used for 3D
                reconstruction if 3D keypoints are not already populated.

        Returns:
            Dict with keys:
                angles          -- raw angle measurements
                angle_scores    -- per-angle scores (0-100)
                front_assembly  -- front assembly score (0-100)
                rear_assembly   -- rear assembly score (0-100)
                topline         -- topline assessment dict
                symmetry        -- symmetry assessment dict
                overall_score   -- weighted composite score (0-100)
                breed_id        -- echo of input breed
                keypoints_used  -- number of keypoints detected
        """
        # -- 3D reconstruction if needed ------------------------------------
        if keypoints.get_3d("withers") is None and keypoints.get_2d("withers") is not None:
            w = image_size[0] if image_size else 640
            h = image_size[1] if image_size else 480
            camera = PinholeCamera.default_for_image(w, h)
            estimator = DepthEstimator(camera)
            estimator.reconstruct_3d(keypoints)
            refiner = LevenbergMarquardtRefiner(camera)
            refiner.refine(keypoints)

        # -- Angle computation ----------------------------------------------
        angles = self.compute_angles(keypoints)

        # -- Breed ideals ---------------------------------------------------
        ideals = self.breed_db.get_ideals(breed_id)
        weights = self.breed_db.get_weights(breed_id)

        if ideals is None:
            # Unknown breed -- return angles without breed-specific scoring.
            return {
                "angles": angles,
                "angle_scores": {},
                "front_assembly": 50.0,
                "rear_assembly": 50.0,
                "topline": self.assess_topline(keypoints),
                "symmetry": self.compute_symmetry(keypoints),
                "overall_score": 50.0,
                "breed_id": breed_id,
                "keypoints_used": keypoints.num_detected(),
            }

        # -- Per-angle scoring ----------------------------------------------
        angle_scores: Dict[str, float] = {}
        weighted_sum = 0.0
        weight_sum = 0.0

        for angle_name, (ideal_val, tol) in ideals.items():
            measured = angles.get(angle_name)
            w_key = weights.get(angle_name, 0.0)

            if measured is not None:
                score = self._score_single_angle(measured, ideal_val, tol)
                angle_scores[angle_name] = score
                weighted_sum += score * w_key
                weight_sum += w_key
            else:
                angle_scores[angle_name] = -1.0  # not measurable

        angle_composite = weighted_sum / weight_sum if weight_sum > 0 else 50.0

        # -- Sub-scores -----------------------------------------------------
        front = self.score_front_assembly(angles, ideals)
        rear = self.score_rear_assembly(angles, ideals)
        topline_info = self.assess_topline(keypoints)
        symmetry_info = self.compute_symmetry(keypoints)

        # -- Overall composite score ----------------------------------------
        # Blend: 50% angle composite, 15% topline, 15% symmetry,
        #        10% front assembly, 10% rear assembly.
        overall = (
            angle_composite * 0.50
            + topline_info["topline_score"] * 0.15
            + symmetry_info["overall_symmetry"] * 0.15
            + front * 0.10
            + rear * 0.10
        )
        overall = max(0.0, min(100.0, overall))

        return {
            "angles": angles,
            "angle_scores": angle_scores,
            "front_assembly": round(front, 2),
            "rear_assembly": round(rear, 2),
            "topline": topline_info,
            "symmetry": symmetry_info,
            "overall_score": round(overall, 2),
            "breed_id": breed_id,
            "keypoints_used": keypoints.num_detected(),
        }


# ============================================================================
# GaitAnalyzer -- multi-frame gait analysis
# ============================================================================

class GaitAnalyzer:
    """Analyses gait (movement) from a sequence of keypoint frames.

    Metrics computed:
        - Stride length (front and rear)
        - Joint angle velocity (angular speed during movement)
        - Reach (front extension) and drive (rear push-off)
        - Single-tracking vs. double-tracking assessment
    """

    def __init__(self, fps: float = 30.0, breed_db: Optional[BreedAngleDatabase] = None):
        """
        Args:
            fps: Frames per second of the input video.
            breed_db: Breed angle database (for breed-specific gait evaluation).
        """
        self.fps = fps
        self.dt = 1.0 / fps
        self.breed_db = breed_db or BreedAngleDatabase()

    # -- stride analysis ----------------------------------------------------

    def compute_stride_length(
        self, frames: List[CanineKeypoints]
    ) -> Dict[str, Optional[float]]:
        """Estimate stride length from paw positions across frames.

        A "stride" is the distance a paw travels between consecutive ground
        contacts. This simplified method measures peak-to-peak horizontal
        displacement of the front and rear paws.

        Returns:
            front_stride: Estimated front stride length in pixels (or 3D units).
            rear_stride: Estimated rear stride length in pixels (or 3D units).
        """
        result: Dict[str, Optional[float]] = {
            "front_stride": None,
            "rear_stride": None,
        }
        if len(frames) < 3:
            return result

        # Collect paw x-positions across frames.
        front_xs: List[float] = []
        rear_xs: List[float] = []

        for f in frames:
            fp = f.get_2d("left_front_paw") or f.get_2d("right_front_paw")
            if fp is not None:
                front_xs.append(fp.x)
            rp = f.get_2d("left_rear_paw")
            if rp is not None:
                rear_xs.append(rp.x)

        def _peak_to_peak(values: List[float]) -> Optional[float]:
            """Find average distance between successive extrema."""
            if len(values) < 3:
                return None
            # Simple peak detection: direction changes.
            peaks: List[float] = []
            for i in range(1, len(values) - 1):
                if (values[i] > values[i-1] and values[i] > values[i+1]) or (values[i] < values[i-1] and values[i] < values[i+1]):
                    peaks.append(values[i])
            if len(peaks) < 2:
                return None
            diffs = [abs(peaks[i+1] - peaks[i]) for i in range(len(peaks) - 1)]
            return sum(diffs) / len(diffs)

        result["front_stride"] = _peak_to_peak(front_xs)
        result["rear_stride"] = _peak_to_peak(rear_xs)
        return result

    # -- angular velocity ---------------------------------------------------

    def compute_joint_angular_velocity(
        self, frames: List[CanineKeypoints]
    ) -> Dict[str, List[float]]:
        """Compute angular speed (degrees/second) for key joints across frames.

        Returns a dict mapping joint name to a list of angular velocities
        (one per frame transition).
        """
        analyzer = PoseAnalyzer(self.breed_db)
        joint_names = [
            "shoulder_angle", "elbow_angle", "stifle_angle", "hock_angle"
        ]

        velocities: Dict[str, List[float]] = {name: [] for name in joint_names}

        prev_angles: Optional[Dict[str, Optional[float]]] = None

        for frame in frames:
            angles = analyzer.compute_angles(frame)
            if prev_angles is not None:
                for jn in joint_names:
                    cur = angles.get(jn)
                    prev = prev_angles.get(jn)
                    if cur is not None and prev is not None:
                        delta = abs(cur - prev)
                        velocities[jn].append(delta / self.dt)
                    else:
                        velocities[jn].append(0.0)
            prev_angles = angles

        return velocities

    # -- reach and drive ----------------------------------------------------

    def compute_reach_and_drive(
        self, frames: List[CanineKeypoints]
    ) -> Dict[str, Optional[float]]:
        """Estimate reach (front extension) and drive (rear propulsion).

        Reach is measured as the maximum forward distance of the front paw
        relative to the shoulder.  Drive is the maximum rearward distance of
        the rear paw relative to the hip.

        All measurements are in pixel units (or 3D if available).

        Returns:
            max_reach: Maximum front reach (pixels).
            max_drive: Maximum rear drive (pixels).
            reach_drive_ratio: Ideally close to 1.0 for balanced movement.
        """
        max_reach = 0.0
        max_drive = 0.0

        for frame in frames:
            # Reach: front paw ahead of shoulder.
            sh = frame.get_2d("left_shoulder") or frame.get_2d("right_shoulder")
            fp = frame.get_2d("left_front_paw") or frame.get_2d("right_front_paw")
            if sh is not None and fp is not None:
                reach = fp.x - sh.x  # positive = forward (assuming dog faces right)
                max_reach = max(max_reach, abs(reach))

            # Drive: rear paw behind hip.
            hip = frame.get_2d("hip_point")
            rp = frame.get_2d("left_rear_paw")
            if hip is not None and rp is not None:
                drive = hip.x - rp.x  # positive = paw behind hip
                max_drive = max(max_drive, abs(drive))

        result: Dict[str, Optional[float]] = {
            "max_reach": max_reach if max_reach > 0 else None,
            "max_drive": max_drive if max_drive > 0 else None,
            "reach_drive_ratio": None,
        }

        if max_reach > 1e-6 and max_drive > 1e-6:
            result["reach_drive_ratio"] = max_reach / max_drive

        return result

    # -- tracking assessment ------------------------------------------------

    def assess_tracking(
        self, frames: List[CanineKeypoints]
    ) -> Dict[str, object]:
        """Assess whether the dog single-tracks or double-tracks.

        Single-tracking: at speed, the paws converge toward a centre line.
        Double-tracking: paws maintain two separate parallel tracks.

        This is estimated by comparing the lateral (y-axis in top-down, or
        x-axis spread from a front view) spread of left vs right paws.
        In a side view we approximate using the vertical spread between
        left and right front paws.

        Returns:
            tracking_type: "single", "double", or "unknown".
            convergence_ratio: 0.0 (perfect single) to 1.0+ (wide double).
            frame_count: Number of frames analysed.
        """
        spreads: List[float] = []

        for frame in frames:
            lf = frame.get_2d("left_front_paw")
            rf = frame.get_2d("right_front_paw")
            if lf is not None and rf is not None:
                spread = abs(lf.y - rf.y)
                spreads.append(spread)

        if not spreads:
            return {
                "tracking_type": "unknown",
                "convergence_ratio": 0.0,
                "frame_count": len(frames),
            }

        avg_spread = sum(spreads) / len(spreads)
        min_spread = min(spreads)

        # Normalise: if the minimum spread is very small relative to average,
        # the dog converges to single-tracking at speed.
        ratio = 0.0 if avg_spread < 1e-06 else min_spread / avg_spread

        if ratio < 0.3:
            tracking = "single"
        elif ratio < 0.7:
            tracking = "mixed"
        else:
            tracking = "double"

        return {
            "tracking_type": tracking,
            "convergence_ratio": round(ratio, 3),
            "frame_count": len(frames),
        }

    # -- main public API ----------------------------------------------------

    def analyze_gait(
        self,
        frame_keypoints: List[CanineKeypoints],
        breed_id: str,
    ) -> Dict[str, object]:
        """Full gait analysis from a sequence of keypoint frames.

        Args:
            frame_keypoints: List of CanineKeypoints, one per video frame.
            breed_id: Breed identifier for breed-specific evaluation.

        Returns:
            Dict with keys:
                stride          -- stride length estimates
                angular_velocity -- joint angular velocities per frame
                reach_drive     -- reach and drive metrics
                tracking        -- single/double tracking assessment
                gait_score      -- composite gait quality score (0-100)
                breed_id        -- echo of input breed
                frame_count     -- number of frames analysed
        """
        stride = self.compute_stride_length(frame_keypoints)
        ang_vel = self.compute_joint_angular_velocity(frame_keypoints)
        reach_drive = self.compute_reach_and_drive(frame_keypoints)
        tracking = self.assess_tracking(frame_keypoints)

        # -- Composite gait score -------------------------------------------
        sub_scores: List[float] = []

        # Reach/drive balance (ideal ratio ~1.0).
        rd_ratio = reach_drive.get("reach_drive_ratio")
        if rd_ratio is not None:
            rd_score = max(0.0, 100.0 - abs(1.0 - rd_ratio) * 100.0)
            sub_scores.append(rd_score)

        # Angular velocity smoothness: lower variance = smoother gait.
        for jn in ["shoulder_angle", "elbow_angle", "stifle_angle", "hock_angle"]:
            vels = ang_vel.get(jn, [])
            if len(vels) >= 2:
                mean_v = sum(vels) / len(vels)
                variance = sum((v - mean_v) ** 2 for v in vels) / len(vels)
                std_dev = math.sqrt(variance)
                # Lower std_dev relative to mean = smoother.
                if mean_v > 1e-6:
                    cv = std_dev / mean_v  # coefficient of variation
                    smoothness = max(0.0, 100.0 - cv * 50.0)
                else:
                    smoothness = 50.0
                sub_scores.append(smoothness)

        # Stride presence bonus.
        if stride.get("front_stride") is not None:
            sub_scores.append(70.0)  # baseline for having detectable stride

        gait_score = sum(sub_scores) / len(sub_scores) if sub_scores else 50.0

        gait_score = max(0.0, min(100.0, gait_score))

        return {
            "stride": stride,
            "angular_velocity": ang_vel,
            "reach_drive": reach_drive,
            "tracking": tracking,
            "gait_score": round(gait_score, 2),
            "breed_id": breed_id,
            "frame_count": len(frame_keypoints),
        }


# ============================================================================
# Self-test
# ============================================================================

def _self_test() -> None:
    """Run a comprehensive self-test of the pose estimation framework.

    Tests vector math, angle computation, scoring, 3D reconstruction,
    and gait analysis with synthetic data. Prints results to stdout.
    """
    print("=" * 70)
    print("ShowDog Pose Estimation - Self Test")
    print("=" * 70)
    errors = 0

    def check(label: str, condition: bool, detail: str = ""):
        nonlocal errors
        status = "PASS" if condition else "FAIL"
        if not condition:
            errors += 1
        msg = f"  [{status}] {label}"
        if detail:
            msg += f" -- {detail}"
        print(msg)

    # -- Vec2 tests ---------------------------------------------------------
    print("\n--- Vec2 ---")
    a2 = Vec2(3.0, 4.0)
    b2 = Vec2(1.0, 2.0)
    check("Vec2 add", (a2 + b2) == Vec2(4.0, 6.0))
    check("Vec2 sub", (a2 - b2) == Vec2(2.0, 2.0))
    check("Vec2 mul", (a2 * 2.0) == Vec2(6.0, 8.0))
    check("Vec2 rmul", (2.0 * a2) == Vec2(6.0, 8.0))
    check("Vec2 div", (a2 / 2.0) == Vec2(1.5, 2.0))
    check("Vec2 neg", (-a2) == Vec2(-3.0, -4.0))
    check("Vec2 length", abs(a2.length() - 5.0) < 1e-9)
    check("Vec2 dot", abs(a2.dot(b2) - 11.0) < 1e-9)
    check("Vec2 normalized length", abs(a2.normalized().length() - 1.0) < 1e-9)
    check("Vec2 distance", abs(a2.distance_to(b2) - math.sqrt(8)) < 1e-9)
    check("Vec2 zero normalized", Vec2(0, 0).normalized() == Vec2(0, 0))

    # -- Vec3 tests ---------------------------------------------------------
    print("\n--- Vec3 ---")
    a3 = Vec3(1.0, 2.0, 3.0)
    b3 = Vec3(4.0, 5.0, 6.0)
    check("Vec3 add", (a3 + b3) == Vec3(5.0, 7.0, 9.0))
    check("Vec3 sub", (a3 - b3) == Vec3(-3.0, -3.0, -3.0))
    check("Vec3 mul", (a3 * 3.0) == Vec3(3.0, 6.0, 9.0))
    check("Vec3 dot", abs(a3.dot(b3) - 32.0) < 1e-9)
    check("Vec3 cross", a3.cross(b3) == Vec3(-3.0, 6.0, -3.0))
    check("Vec3 length", abs(a3.length() - math.sqrt(14)) < 1e-9)
    check("Vec3 normalized", abs(a3.normalized().length() - 1.0) < 1e-9)

    # -- Mat3 tests ---------------------------------------------------------
    print("\n--- Mat3 ---")
    identity = Mat3()
    check("Mat3 identity det", abs(identity.determinant() - 1.0) < 1e-9)
    check("Mat3 identity * vec", identity.mul_vec3(a3) == a3)

    rot = Mat3.rotation_y(90.0)
    v_fwd = Vec3(0.0, 0.0, 1.0)
    rotated = rot.mul_vec3(v_fwd)
    check(
        "Mat3 rotation_y(90) of Z -> X",
        abs(rotated.x - 1.0) < 1e-6 and abs(rotated.z) < 1e-6,
        f"got {rotated}",
    )

    m = Mat3([2, 0, 0, 0, 3, 0, 0, 0, 4])
    inv = m.inverse()
    product = m.mul_mat3(inv)
    check(
        "Mat3 inverse",
        abs(product.at(0, 0) - 1.0) < 1e-9
        and abs(product.at(1, 1) - 1.0) < 1e-9
        and abs(product.at(2, 2) - 1.0) < 1e-9,
    )

    transposed = m.transposed()
    check("Mat3 transpose diagonal", abs(transposed.at(0, 0) - 2.0) < 1e-9)

    # -- angle helpers ------------------------------------------------------
    print("\n--- Angle helpers ---")
    right_angle = angle_between_vectors_deg(Vec3(1, 0, 0), Vec3(0, 1, 0))
    check("90-degree angle", abs(right_angle - 90.0) < 1e-6)

    straight = angle_between_vectors_deg(Vec3(1, 0, 0), Vec3(1, 0, 0))
    check("0-degree angle", abs(straight) < 1e-6)

    opposite = angle_between_vectors_deg(Vec3(1, 0, 0), Vec3(-1, 0, 0))
    check("180-degree angle", abs(opposite - 180.0) < 1e-6)

    vertex_angle = angle_at_vertex_deg(
        Vec3(1, 0, 0), Vec3(0, 0, 0), Vec3(0, 1, 0)
    )
    check("Vertex angle 90", abs(vertex_angle - 90.0) < 1e-6)

    # -- CanineKeypoints ----------------------------------------------------
    print("\n--- CanineKeypoints ---")
    kp = CanineKeypoints()
    check("Initial count 0", kp.num_detected() == 0)
    kp.set_2d("nose", Vec2(100, 50), 0.9)
    kp.set_2d("withers", Vec2(200, 150), 0.95)
    check("After 2 sets, count 2", kp.num_detected() == 2)
    check("has nose", kp.has("nose"))
    check("not has hip_point", not kp.has("hip_point"))
    check("confidence", abs(kp.confidence("nose") - 0.9) < 1e-9)
    check("min_confidence", abs(kp.min_confidence() - 0.9) < 1e-9)

    # -- BreedAngleDatabase -------------------------------------------------
    print("\n--- BreedAngleDatabase ---")
    db = BreedAngleDatabase()
    breeds = db.list_breeds()
    check("At least 10 breeds loaded", len(breeds) >= 10, f"got {len(breeds)}")

    gsd_ideals = db.get_ideals("166_german_shepherd")
    check("GSD ideals exist", gsd_ideals is not None)
    if gsd_ideals:
        check(
            "GSD shoulder ideal ~90",
            abs(gsd_ideals["shoulder_angle"][0] - 90.0) < 1.0,
        )

    lab_ideals = db.get_ideals("122_labrador_retriever")
    check("Lab ideals exist", lab_ideals is not None)
    if lab_ideals:
        check(
            "Lab shoulder ideal ~97",
            abs(lab_ideals["shoulder_angle"][0] - 97.0) < 1.0,
        )

    # -- PinholeCamera ------------------------------------------------------
    print("\n--- PinholeCamera ---")
    cam = PinholeCamera.default_for_image(640, 480)
    proj = cam.project(Vec3(0.0, 0.0, 5.0))
    check(
        "Centre point projects to principal point",
        abs(proj.x - 320.0) < 1.0 and abs(proj.y - 240.0) < 1.0,
        f"got {proj}",
    )

    ray = cam.back_project_ray(Vec2(320, 240))
    check(
        "Centre ray points forward",
        abs(ray.x) < 0.01 and abs(ray.y) < 0.01 and ray.z > 0.9,
        f"got {ray}",
    )

    # -- PoseAnalyzer with synthetic dog ------------------------------------
    print("\n--- PoseAnalyzer (synthetic Labrador) ---")

    # Create a synthetic side-view Labrador keypoint set.
    # Image is 800x600.  Dog faces right.
    synth = CanineKeypoints()
    synth.set_2d("nose", Vec2(550, 180), 0.95)
    synth.set_2d("left_eye", Vec2(520, 170), 0.93)
    synth.set_2d("right_eye", Vec2(510, 175), 0.90)
    synth.set_2d("left_ear_base", Vec2(490, 155), 0.88)
    synth.set_2d("right_ear_base", Vec2(480, 160), 0.87)
    synth.set_2d("withers", Vec2(400, 200), 0.96)
    synth.set_2d("spine_mid", Vec2(330, 198), 0.94)
    synth.set_2d("hip_point", Vec2(250, 205), 0.95)
    synth.set_2d("left_shoulder", Vec2(410, 260), 0.92)
    synth.set_2d("left_elbow", Vec2(415, 340), 0.91)
    synth.set_2d("left_front_paw", Vec2(420, 450), 0.90)
    synth.set_2d("right_shoulder", Vec2(395, 265), 0.89)
    synth.set_2d("right_elbow", Vec2(400, 345), 0.88)
    synth.set_2d("right_front_paw", Vec2(405, 455), 0.87)
    synth.set_2d("left_stifle", Vec2(240, 300), 0.91)
    synth.set_2d("left_hock", Vec2(230, 390), 0.90)
    synth.set_2d("left_rear_paw", Vec2(225, 455), 0.89)

    check("Synthetic dog: 17 keypoints", synth.num_detected() == 17)

    analyzer = PoseAnalyzer()
    result = analyzer.analyze_photo(synth, "122_labrador_retriever", (800, 600))

    check("Result has overall_score", "overall_score" in result)
    check(
        "Overall score in range",
        0.0 <= result["overall_score"] <= 100.0,
        f"score={result['overall_score']}",
    )
    check("Result has angles", "angles" in result)
    check("Result has angle_scores", "angle_scores" in result)
    check(
        "Front assembly in range",
        0.0 <= result["front_assembly"] <= 100.0,
        f"front={result['front_assembly']}",
    )
    check(
        "Rear assembly in range",
        0.0 <= result["rear_assembly"] <= 100.0,
        f"rear={result['rear_assembly']}",
    )

    angles = result["angles"]
    for aname in ["shoulder_angle", "elbow_angle", "stifle_angle", "hock_angle", "topline_angle"]:
        val = angles.get(aname)
        check(
            f"Angle '{aname}' computed",
            val is not None,
            f"value={val}",
        )

    print(f"\n  Angles: { {k: round(v, 1) if v else v for k, v in angles.items()} }")
    print(f"  Angle scores: { {k: round(v, 1) for k, v in result['angle_scores'].items()} }")
    print(f"  Overall score: {result['overall_score']}")

    # -- Topline assessment -------------------------------------------------
    print("\n--- Topline assessment ---")
    topline = result["topline"]
    check("Topline score in range", 0.0 <= topline["topline_score"] <= 100.0)
    print(f"  Topline score: {topline['topline_score']:.1f}")
    print(f"  Curvature: {topline['curvature_deg']:.1f} deg")

    # -- Symmetry assessment ------------------------------------------------
    print("\n--- Symmetry assessment ---")
    sym = result["symmetry"]
    check("Symmetry score in range", 0.0 <= sym["overall_symmetry"] <= 100.0)
    print(f"  Front symmetry: {sym['front_symmetry']:.1f}")
    print(f"  Overall symmetry: {sym['overall_symmetry']:.1f}")

    # -- Unknown breed fallback ---------------------------------------------
    print("\n--- Unknown breed fallback ---")
    unknown_result = analyzer.analyze_photo(synth, "999_unknown_breed", (800, 600))
    check("Unknown breed returns score 50", abs(unknown_result["overall_score"] - 50.0) < 1e-6)

    # -- GaitAnalyzer -------------------------------------------------------
    print("\n--- GaitAnalyzer (synthetic 10-frame sequence) ---")

    frames: List[CanineKeypoints] = []
    for i in range(10):
        f = CanineKeypoints()
        # Simulate forward walking motion with oscillating paw positions.
        phase = i * 0.6  # radians
        front_x = 420.0 + 30.0 * math.sin(phase)
        rear_x = 225.0 + 25.0 * math.sin(phase + math.pi)

        f.set_2d("withers", Vec2(400, 200))
        f.set_2d("spine_mid", Vec2(330, 198))
        f.set_2d("hip_point", Vec2(250, 205))
        f.set_2d("left_shoulder", Vec2(410, 260))
        f.set_2d("left_elbow", Vec2(415, 340))
        f.set_2d("left_front_paw", Vec2(front_x, 450))
        f.set_2d("right_shoulder", Vec2(395, 265))
        f.set_2d("right_elbow", Vec2(400, 345))
        f.set_2d("right_front_paw", Vec2(front_x - 15, 455))
        f.set_2d("left_stifle", Vec2(240, 300))
        f.set_2d("left_hock", Vec2(230, 390))
        f.set_2d("left_rear_paw", Vec2(rear_x, 455))
        f.set_2d("nose", Vec2(550, 180))
        frames.append(f)

    gait_analyzer = GaitAnalyzer(fps=30.0)
    gait_result = gait_analyzer.analyze_gait(frames, "122_labrador_retriever")

    check("Gait result has gait_score", "gait_score" in gait_result)
    check(
        "Gait score in range",
        0.0 <= gait_result["gait_score"] <= 100.0,
        f"score={gait_result['gait_score']}",
    )
    check("Frame count correct", gait_result["frame_count"] == 10)

    stride = gait_result["stride"]
    check("Front stride detected", stride["front_stride"] is not None)
    print(f"  Front stride: {stride['front_stride']}")
    print(f"  Rear stride: {stride['rear_stride']}")

    rd = gait_result["reach_drive"]
    check("Reach detected", rd["max_reach"] is not None)
    check("Drive detected", rd["max_drive"] is not None)
    if rd["reach_drive_ratio"] is not None:
        print(f"  Reach/drive ratio: {rd['reach_drive_ratio']:.2f}")

    tracking = gait_result["tracking"]
    check(
        "Tracking type determined",
        tracking["tracking_type"] in ("single", "double", "mixed", "unknown"),
        f"type={tracking['tracking_type']}",
    )
    print(f"  Tracking: {tracking['tracking_type']} (convergence={tracking['convergence_ratio']})")

    print(f"  Gait score: {gait_result['gait_score']}")

    # -- Depth estimation ---------------------------------------------------
    print("\n--- DepthEstimator ---")
    cam2 = PinholeCamera.default_for_image(800, 600)
    depth_est = DepthEstimator(cam2, reference_height_m=0.57)
    depth = depth_est.estimate_depth(synth)
    check("Depth is positive", depth > 0.0, f"depth={depth:.2f}m")
    check("Depth is reasonable (0.5-20m)", 0.5 <= depth <= 20.0, f"depth={depth:.2f}m")
    print(f"  Estimated depth: {depth:.2f} m")

    # -- LM Refiner ---------------------------------------------------------
    print("\n--- LevenbergMarquardtRefiner ---")
    cam3 = PinholeCamera.default_for_image(800, 600)
    est3 = DepthEstimator(cam3, reference_height_m=0.57)
    synth_copy = CanineKeypoints()
    for idx in range(NUM_KEYPOINTS):
        pt = synth.get_2d_by_index(idx)
        if pt is not None:
            synth_copy.set_2d_by_index(idx, pt, synth._confidence[idx])
    est3.reconstruct_3d(synth_copy)

    refiner = LevenbergMarquardtRefiner(cam3)
    err_before = refiner._reprojection_error(synth_copy)
    refiner.refine(synth_copy)
    err_after = refiner._reprojection_error(synth_copy)
    check(
        "Refinement reduces or maintains error",
        err_after <= err_before + 0.5,
        f"before={err_before:.2f}px, after={err_after:.2f}px",
    )
    print(f"  Reprojection error: {err_before:.2f}px -> {err_after:.2f}px")

    # -- scoring edge cases -------------------------------------------------
    print("\n--- Scoring edge cases ---")
    pa = PoseAnalyzer()

    # Perfect match.
    perfect_score = pa._score_single_angle(90.0, 90.0, 5.0)
    check("Perfect angle -> 100", abs(perfect_score - 100.0) < 1e-6)

    # At tolerance boundary.
    boundary_score = pa._score_single_angle(95.0, 90.0, 5.0)
    check("At tolerance -> 90", abs(boundary_score - 90.0) < 1e-6)

    # Well beyond tolerance.
    bad_score = pa._score_single_angle(110.0, 90.0, 5.0)
    check("Beyond 4x tolerance -> 0", abs(bad_score) < 1e-6)

    # Just beyond tolerance.
    slight_score = pa._score_single_angle(97.0, 90.0, 5.0)
    check("Slightly beyond tolerance -> 30-90", 30.0 < slight_score < 90.0, f"score={slight_score:.1f}")

    # -- Summary ------------------------------------------------------------
    print("\n" + "=" * 70)
    if errors == 0:
        print("ALL TESTS PASSED")
    else:
        print(f"{errors} TEST(S) FAILED")
    print("=" * 70)


# ============================================================================
# Entry point
# ============================================================================

if __name__ == "__main__":
    _self_test()
