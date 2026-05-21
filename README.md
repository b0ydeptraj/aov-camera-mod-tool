# AoV / Liên Quân Camera Mod Tool

Tool GUI Windows để vá `CommonActions.pkg.bytes` và chỉnh camera xa hơn.

## Tải bản exe

Mở tab **Releases** của repo này và tải bản mới nhất.

## Mức camera trong GUI

- `10%` = giá trị kỹ thuật `0.75`
- `20%` = giá trị kỹ thuật `1.5`
- `40%` = giá trị kỹ thuật `3.0`

## Cách dùng

1. Mở `Mod_Camera_Lien_Quan.exe`.
2. Chọn `CommonActions.pkg.bytes` hoặc chọn thư mục `Ages` / `Resources`.
3. Chọn `kgvn.app` hoặc `kgvn.app\Data\resources.assets` của đúng bản game update.
4. Chọn nơi lưu file đã mod.
5. Chọn mức camera rồi bấm `Mod ngay`.

Tool tự đọc `dict id` trong `CommonActions.pkg.bytes`, quét `resources.assets`, dò đúng raw zstd dictionary và verify bằng XML bên trong package. Tool không dùng `zstd_dict.bin` mặc định cũ.

## Đường dẫn file trong game

CommonActions:

```text
Documents\Resources\1.62.1\Ages\Prefab_Characters\Prefab_Hero\CommonActions.pkg.bytes
```

Raw dictionary trong IPA/app:

```text
kgvn.app\Data\resources.assets
```

## Source

Chạy bằng Python:

```powershell
python patch_camera_gui.py
```

CLI:

```powershell
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --game-assets "C:\path\kgvn.app" --height 1.5 --output "C:\path\CommonActions_patched.pkg.bytes"
```
