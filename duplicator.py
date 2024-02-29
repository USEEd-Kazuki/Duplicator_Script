import unreal
import os
import time

start_time = time.time()

editor_util = unreal.EditorUtilityLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

# 選択中のアセット取得

selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)

# 複製する個数を入力
num_copies = 50
total_num_copies = num_assets * num_copies
text_label = "Dulicating Assets"
running = True

# SlowTask を使って進捗状況を表示
with unreal.ScopedSlowTask(total_num_copies, text_label) as slow_task:
    
    slow_task.make_dialog(True)

    # 選択されたアセットをループ処理
    for asset in selected_assets:
        asset_name = asset.get_fname()
        asset_path = editor_asset_lib.get_path_name_for_loaded_asset(asset)
        source_path = os.path.dirname(asset_path)

        for i in range(num_copies):
             # キャンセルされたかどうかを確認
            if slow_task.should_cancel():
                running = False
                break
            new_name = "{}_{}".format(asset_name, i)
            dest_path = os.path.join(source_path, new_name)
            duplicate = editor_asset_lib.duplicate_asset(asset_path, dest_path)
             # 進捗状況を更新
            slow_task.enter_progress_frame(1) 

            if duplicate is None:
                unreal.log_warning("Duplicate from {} at {} already exists".format(source_path, dest_path))
            unreal.log("{}_{}".format(asset_name , i))
        
        if not running:
            break

    end_time = time.time()
    # 実行時間と複製したアセットの情報をログに出力
    unreal.log("{} asset/s duplicated {} times in {} seconds".format(num_assets, num_copies, end_time - start_time))