# -*- coding: utf-8 -*-
"""
DBの座標のダンプファイルを用い、リサイズ、座標調整、グレースケースケール画像保存、学習用ファイルを生成する。
"""
import common_image
import cv2
import os

def resize_adjust_coordinate(db_result, target_image_dir, out_dir_resize, out_dir_gray, insize_tuple, resize_tuple, adjust_rate, out_training_csv):
    with open(out_training_csv, 'a') as out_f:
        out_f.write('left_top_x,left_top_y,right_top_x,right_top_y,left_middle_x,left_middle_y,right_middle_x,right_middle_y,left_bottom_x,left_bottom_y,right_bottom_x,right_bottom_y,Image\n')

    with open(db_result, 'r') as dbfile:
        for line in dbfile:
            line = line.rstrip()
            values = line.split('\t')
            id = values[0]          # image_id
            image_path = values[2]  # image_path
            processed = values[3]   # 処理済みフラグ

            if id == 'image_id':
                continue

            if processed == '1':
                left_top_x = values[4]       # 左上x座標
                left_top_y = values[5]       # 左上y座標
                right_top_x = values[6]      # 右上x座標
                right_top_y = values[7]      # 右上x座標
                left_middle_x = values[8]    # 左中央x座標
                left_middle_y = values[9]    # 左中央y座標
                right_middle_x = values[10]  # 右中x座標
                right_middle_y = values[11]  # 右中央y座標
                left_bottom_x = values[12]   # 左下x座標
                left_bottom_y = values[13]   # 左下y座標
                right_bottom_x = values[14]  # 右下x座標
                right_bottom_y = values[15]  # 右下y座標

                left_top = (left_top_x, left_top_y)
                right_top = (right_top_x, right_top_y)
                left_middle = (left_middle_x, left_middle_y)
                right_middle = (right_middle_x, right_middle_y)
                left_bottom = (left_bottom_x, left_bottom_y)
                right_bottom = (right_bottom_x, right_bottom_y)

                left_top_adjust = common_image.resize_coordinate(left_top, adjust_rate)
                right_top_adjust = common_image.resize_coordinate(right_top, adjust_rate)
                left_middle_adjust = common_image.resize_coordinate(left_middle, adjust_rate)
                right_middle_adjust = common_image.resize_coordinate(right_middle, adjust_rate)
                left_bottom_adjust = common_image.resize_coordinate(left_bottom, adjust_rate)
                right_bottom_adjust = common_image.resize_coordinate(right_bottom, adjust_rate)

                coordinate_list = [left_top_adjust, right_top_adjust, left_middle_adjust,
                                   right_middle_adjust, left_bottom_adjust, right_bottom_adjust]

                image_name = image_path.split('/')[-1]
                image = cv2.imread(target_image_dir + image_name)

                resize_image = common_image.resize_image(image, resize_tuple)
                save_name = out_dir_resize + '/' + image_name
                common_image.save_image(resize_image, save_name)

                gray_image = common_image.gray_convert(resize_image)
                image_name = image_name.replace('_' + str(insize_tuple[0]), '_' + str(resize_tuple[0]))\
                    .replace('_' + str(insize_tuple[1]), '_' + str(resize_tuple[1]))
                save_gray_image_name = out_dir_gray + 'gray_' + image_name
                common_image.save_image(gray_image, save_gray_image_name)

                common_image.make_training_data_from_gray_image(coordinate_list, gray_image, out_training_csv, save_gray_image_name)



if __name__ == '__main__':
    """
    db_result：MYSQLのDBダンプファイル
    target_image_dir：リサイズしたい画像のディレクトリ
    out_dir_resize：リサイズ後のカラーイメージ保存ディレクトリ
    out_dir_gray：リサイズ後のグレースケールイメージ保存ディレクトリ
    insize_tuple：inputの画像のサイズ(width, height)
    resize_tuple：リサイズするサイズ(width, height)
    adjust_rate：リサイズする割合(width, height)
    """
    root_dir = '/usr/local/wk/git_local/bike/'
    db_result = root_dir + 'analysis/front_fork/data/from_db/bike_result_20170412_right.tsv'
    target_image_dir = root_dir + 'analysis/front_fork/data/images/training_image/right_resize/'
    out_dir_resize = root_dir + 'analysis/front_fork/data/images/training_image/right_resize_150_200/'
    if not os.path.exists(out_dir_resize):
        os.mkdir(out_dir_resize)
    out_dir_gray = root_dir + 'analysis/front_fork/data/images/training_image/right_resize_150_200_gray/'
    if not os.path.exists(out_dir_gray):
        os.mkdir(out_dir_gray)
    insize_tuple = (400, 300)
    resize_tuple = (200, 150)
    adjust_rate = (0.5, 0.5)
    out_training_csv = root_dir + 'analysis/front_fork/data/train/right/bike_training_150_200_conf.csv'
    resize_adjust_coordinate(db_result, target_image_dir, out_dir_resize, out_dir_gray,
                             insize_tuple, resize_tuple, adjust_rate, out_training_csv)
