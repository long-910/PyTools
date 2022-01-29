# -*- coding: utf-8 -*-
"""
参考 [here](https://self-development.info/python%E3%81%A7%E6%8C%87%E5%AE%9A%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E4%BB%A5%E4%B8%8B%E3%81%AB%E3%81%82%E3%82%8B%E7%94%BB%E5%83%8F%E3%81%AEexif%E6%83%85%E5%A0%B1%E3%82%92%E5%89%8A%E9%99%A4%E3%81%99/)
"""
import argparse
from pathlib import Path
import re
from xml.etree.ElementTree import tostring
from PIL import Image

TARGET_DIR = "."

def get_image_path_list(target):
    # 結果用リスト初期化
    result_list = []
    # Pathクラス利用
    path = Path(target)
    # target以下のすべてのパス（フォルダ・ファイル含め）
    all_path_list = path.glob('**/*')
    # 拡張子が画像ファイルであれば画像パスと判定する
    # 大文字（例えば、test.JPG）でも画像と判定する
    for p in all_path_list:
        hit = re.search('/*\.(jpg|jpeg|png|gif|bmp)', str(p), flags=re.IGNORECASE)
        if hit:
            result_list.append(p)

    return result_list

def eraser_exif(file):
    # 画像を開く
    with Image.open(file) as src:
        # 次の3つを取得
        data = src.getdata()
        mode = src.mode
        size = src.size

        # 上記で取得したデータをもとに新規で画像を作成＝上書き
        with Image.new(mode, size) as dst:
            dst.putdata(data)
            dst.save(file)
            print(file)

def main():
    parser = argparse.ArgumentParser(description='Delete Image EXIF')
    parser.add_argument('tgtFolder', help='Target Folder')
    args = parser.parse_args()

    image_path_list = get_image_path_list(args.tgtFolder)

    for image_path in image_path_list:
        eraser_exif(image_path)

if __name__ == "__main__":
    main()