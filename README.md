# AoV / Liên Quân Camera Mod Tool

Tool GUI Windows để vá `CommonActions.pkg.bytes` và chỉnh camera xa hơn.

## Tải bản exe

Mở tab **Releases** của repo này và tải `Mod_Camera_Lien_Quan_v1.0.0.zip`.

## Mức camera trong GUI

- `10%` = giá trị kỹ thuật `0.75`
- `20%` = giá trị kỹ thuật `1.5`
- `40%` = giá trị kỹ thuật `3.0`

## Cách dùng

1. Mở `Mod_Camera_Lien_Quan.exe`.
2. Chọn `CommonActions.pkg.bytes` hoặc chọn thư mục `Ages` / `Resources`.
3. Chọn dictionary, bình thường dùng mặc định trong tool. Nếu chọn nhầm `bytesDict.bytes` của game, tool sẽ tự thử lại bằng dictionary mặc định.
4. Chọn nơi lưu file đã mod.
5. Chọn mức camera rồi bấm `Mod ngay`.

## Đường dẫn file trong game

CommonActions:

```text
Documents\Resources\1.62.1\Ages\Prefab_Characters\Prefab_Hero\CommonActions.pkg.bytes
```

bytesDict khi game update đổi dictionary:

```text
Documents\Resources\1.62.1\Config\bytesDict.bytes
```

## Source

Chạy bằng Python:

```powershell
python patch_camera_gui.py
```

CLI:

```powershell
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --height 1.5
```
