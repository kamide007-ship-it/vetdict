#!/bin/bash
# Renderデプロイ後のテストスクリプト

echo "=================================="
echo "ShowDog v3.1 - Render テスト"
echo "=================================="
echo ""

# URLを入力
read -p "Render URL を入力してください (例: https://your-app.onrender.com): " RENDER_URL

echo ""
echo "Test 1: Health Check"
echo "-----------------------------------"
curl -s $RENDER_URL/api/health | python3 -m json.tool

echo ""
echo ""
echo "Test 2: Breeds List"
echo "-----------------------------------"
curl -s $RENDER_URL/api/breeds | python3 -m json.tool | head -20

echo ""
echo ""
echo "Test 3: Web Interface"
echo "-----------------------------------"
echo "ブラウザで以下にアクセスしてください:"
echo "$RENDER_URL/"
echo ""

echo "=================================="
echo "テスト完了"
echo "=================================="
