"""
Tests for the 3D pose estimation framework.

Tests cover:
- Vec2 and Vec3 vector math
- Mat3 matrix operations
- Angle calculations
- CanineKeypoints data structure
- BreedAngleDatabase
- PoseAnalyzer scoring
"""

import pytest

from api.pose_estimation import (
    KEYPOINT_NAMES,
    KP,
    NUM_KEYPOINTS,
    BreedAngleDatabase,
    CanineKeypoints,
    Mat3,
    Vec2,
    Vec3,
    angle_at_vertex_2d_deg,
    angle_at_vertex_deg,
    angle_between_vectors_deg,
)


# ============================================================================
# Vec2
# ============================================================================


class TestVec2:
    def test_create(self):
        v = Vec2(3.0, 4.0)
        assert v.x == 3.0
        assert v.y == 4.0

    def test_add(self):
        a = Vec2(1, 2)
        b = Vec2(3, 4)
        c = a + b
        assert c.x == 4.0
        assert c.y == 6.0

    def test_sub(self):
        a = Vec2(5, 7)
        b = Vec2(2, 3)
        c = a - b
        assert c.x == 3.0
        assert c.y == 4.0

    def test_mul(self):
        v = Vec2(3, 4) * 2
        assert v.x == 6.0
        assert v.y == 8.0

    def test_rmul(self):
        v = 2 * Vec2(3, 4)
        assert v.x == 6.0

    def test_div(self):
        v = Vec2(6, 8) / 2
        assert v.x == 3.0
        assert v.y == 4.0

    def test_neg(self):
        v = -Vec2(3, 4)
        assert v.x == -3.0
        assert v.y == -4.0

    def test_length(self):
        v = Vec2(3, 4)
        assert abs(v.length() - 5.0) < 1e-9

    def test_length_zero(self):
        v = Vec2(0, 0)
        assert v.length() == 0.0

    def test_dot(self):
        a = Vec2(1, 0)
        b = Vec2(0, 1)
        assert a.dot(b) == 0.0

    def test_normalized(self):
        v = Vec2(3, 4).normalized()
        assert abs(v.length() - 1.0) < 1e-9

    def test_normalized_zero(self):
        v = Vec2(0, 0).normalized()
        assert v.length() == 0.0

    def test_distance_to(self):
        a = Vec2(0, 0)
        b = Vec2(3, 4)
        assert abs(a.distance_to(b) - 5.0) < 1e-9

    def test_immutable(self):
        v = Vec2(1, 2)
        with pytest.raises(AttributeError):
            v.x = 3

    def test_equality(self):
        assert Vec2(1, 2) == Vec2(1, 2)
        assert Vec2(1, 2) != Vec2(1, 3)

    def test_as_tuple(self):
        assert Vec2(1, 2).as_tuple() == (1.0, 2.0)

    def test_angle_to_horizontal(self):
        v = Vec2(1, 0)
        assert abs(v.angle_to_horizontal()) < 1e-9
        v2 = Vec2(0, 1)
        assert abs(v2.angle_to_horizontal() - 90.0) < 1e-9


# ============================================================================
# Vec3
# ============================================================================


class TestVec3:
    def test_create(self):
        v = Vec3(1, 2, 3)
        assert v.x == 1.0

    def test_add(self):
        c = Vec3(1, 2, 3) + Vec3(4, 5, 6)
        assert c.x == 5.0 and c.y == 7.0 and c.z == 9.0

    def test_sub(self):
        c = Vec3(5, 7, 9) - Vec3(1, 2, 3)
        assert c.x == 4.0 and c.y == 5.0 and c.z == 6.0

    def test_length(self):
        v = Vec3(1, 2, 2)
        assert abs(v.length() - 3.0) < 1e-9

    def test_dot(self):
        a = Vec3(1, 0, 0)
        b = Vec3(0, 1, 0)
        assert a.dot(b) == 0.0

    def test_cross(self):
        a = Vec3(1, 0, 0)
        b = Vec3(0, 1, 0)
        c = a.cross(b)
        assert c == Vec3(0, 0, 1)

    def test_normalized(self):
        v = Vec3(3, 4, 0).normalized()
        assert abs(v.length() - 1.0) < 1e-9

    def test_immutable(self):
        v = Vec3(1, 2, 3)
        with pytest.raises(AttributeError):
            v.x = 0

    def test_equality(self):
        assert Vec3(1, 2, 3) == Vec3(1, 2, 3)

    def test_distance_to(self):
        a = Vec3(0, 0, 0)
        b = Vec3(1, 2, 2)
        assert abs(a.distance_to(b) - 3.0) < 1e-9


# ============================================================================
# Mat3
# ============================================================================


class TestMat3:
    def test_identity(self):
        m = Mat3()
        assert m.at(0, 0) == 1.0
        assert m.at(0, 1) == 0.0
        assert m.at(1, 1) == 1.0

    def test_custom_values(self):
        m = Mat3([1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert m.at(0, 0) == 1.0
        assert m.at(2, 2) == 9.0

    def test_wrong_size_raises(self):
        with pytest.raises(ValueError):
            Mat3([1, 2, 3])

    def test_mul_vec3_identity(self):
        m = Mat3()
        v = Vec3(1, 2, 3)
        result = m.mul_vec3(v)
        assert result == v

    def test_immutable(self):
        m = Mat3()
        with pytest.raises(AttributeError):
            m.x = 5


# ============================================================================
# Angle Calculations
# ============================================================================


class TestAngleCalculations:
    def test_angle_between_parallel(self):
        a = Vec3(1, 0, 0)
        b = Vec3(2, 0, 0)
        angle = angle_between_vectors_deg(a, b)
        assert abs(angle) < 1e-6

    def test_angle_between_perpendicular(self):
        a = Vec3(1, 0, 0)
        b = Vec3(0, 1, 0)
        angle = angle_between_vectors_deg(a, b)
        assert abs(angle - 90.0) < 1e-6

    def test_angle_between_opposite(self):
        a = Vec3(1, 0, 0)
        b = Vec3(-1, 0, 0)
        angle = angle_between_vectors_deg(a, b)
        assert abs(angle - 180.0) < 1e-6

    def test_angle_at_vertex_3d(self):
        p1 = Vec3(1, 0, 0)
        vertex = Vec3(0, 0, 0)
        p2 = Vec3(0, 1, 0)
        angle = angle_at_vertex_deg(p1, vertex, p2)
        assert abs(angle - 90.0) < 1e-6

    def test_angle_at_vertex_2d(self):
        p1 = Vec2(1, 0)
        vertex = Vec2(0, 0)
        p2 = Vec2(0, 1)
        angle = angle_at_vertex_2d_deg(p1, vertex, p2)
        assert abs(angle - 90.0) < 1e-6

    def test_straight_angle_2d(self):
        p1 = Vec2(1, 0)
        vertex = Vec2(0, 0)
        p2 = Vec2(-1, 0)
        angle = angle_at_vertex_2d_deg(p1, vertex, p2)
        assert abs(angle - 180.0) < 1e-6


# ============================================================================
# Keypoints
# ============================================================================


class TestCanineKeypoints:
    def test_keypoint_count(self):
        assert NUM_KEYPOINTS == 17

    def test_keypoint_names(self):
        assert "nose" in KEYPOINT_NAMES
        assert "withers" in KEYPOINT_NAMES
        assert "hip_point" in KEYPOINT_NAMES
        assert "left_front_paw" in KEYPOINT_NAMES

    def test_kp_map(self):
        assert KP["nose"] == 0
        assert KP["left_rear_paw"] == 16

    def test_create_empty(self):
        kps = CanineKeypoints()
        assert kps is not None

    def test_set_and_get_2d(self):
        kps = CanineKeypoints()
        kps.set_2d("nose", Vec2(320, 100), confidence=0.95)
        nose = kps.get_2d("nose")
        assert nose is not None
        assert abs(nose.x - 320.0) < 1e-9
        assert abs(nose.y - 100.0) < 1e-9

    def test_unset_keypoint_is_none(self):
        kps = CanineKeypoints()
        assert kps.get_2d("withers") is None

    def test_set_2d_by_index(self):
        kps = CanineKeypoints()
        kps.set_2d_by_index(0, Vec2(100, 200), confidence=0.9)
        pt = kps.get_2d_by_index(0)
        assert pt is not None
        assert abs(pt.x - 100.0) < 1e-9


# ============================================================================
# Breed Angle Database
# ============================================================================


class TestBreedAngleDatabase:
    def test_database_has_defaults(self):
        db = BreedAngleDatabase()
        assert db is not None

    def test_get_known_breed(self):
        db = BreedAngleDatabase()
        angles = db.get_ideals("122_labrador_retriever")
        assert isinstance(angles, dict)
        assert len(angles) > 0
        assert "shoulder_angle" in angles

    def test_get_unknown_breed_returns_none(self):
        db = BreedAngleDatabase()
        angles = db.get_ideals("unknown_breed_xyz")
        assert angles is None

    def test_get_weights(self):
        db = BreedAngleDatabase()
        weights = db.get_weights("122_labrador_retriever")
        assert isinstance(weights, dict)
        assert abs(sum(weights.values()) - 1.0) < 0.01
