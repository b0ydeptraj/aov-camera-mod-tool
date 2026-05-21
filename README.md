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
3. Nếu game update, chọn thêm `bytesDict.bytes` và `kgvn.app` hoặc `kgvn.app\Data\resources.assets` để tool tự trích raw dictionary mới.
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

Raw dictionary trong IPA/app:

```text
kgvn.app\Data\resources.assets
```

Lưu ý: `bytesDict.bytes` của game là file bọc riêng/AES, không phải raw dictionary để chọn trực tiếp trong zstd. Tool dùng `bytesDict.bytes` để đọc kích thước, rồi quét `resources.assets` để trích raw zstd dictionary đúng bản và verify `dict id` với `CommonActions.pkg.bytes`.

## Source

Chạy bằng Python:

```powershell
python patch_camera_gui.py
```

CLI:

```powershell
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --height 1.5
```

CLI khi game update đổi dictionary:

```powershell
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --bytes-dict "C:\path\bytesDict.bytes" --game-assets "C:\path\kgvn.app" --height 1.5 --output "C:\path\CommonActions_patched.pkg.bytes"
```
