AoV / Liên Quân Camera Mod Tool

Tool này vá CommonActions.pkg.bytes để chỉnh camera xa hơn.

File được vá:
- commonresource/Dance.xml
- PassiveResource/junglemark.xml

Mức camera trong GUI:
- 10% = giá trị kỹ thuật 0.75
- 20% = giá trị kỹ thuật 1.5
- 40% = giá trị kỹ thuật 3.0

Cách dùng GUI:
1. Mở Mo_Giao_Dien.vbs để không hiện CMD đen.
2. Chọn CommonActions.pkg.bytes hoặc file bị đổi tên kiểu CommonActions.pkg_1.bytes, hoặc chọn thư mục Ages/Resources.
3. Để dictionary mặc định. Ô này cần raw zstd dictionary, còn bytesDict.bytes của game là file bọc riêng.
4. Chọn nơi lưu file đã mod.
5. Chọn mức camera 10%, 20% hoặc 40%, rồi bấm Mod ngay.

Đường dẫn lấy CommonActions trong game:
Documents\Resources\1.62.1\Ages\Prefab_Characters\Prefab_Hero\CommonActions.pkg.bytes

Đường dẫn lấy bytesDict nếu game update đổi dictionary để phân tích/cập nhật tool:
Documents\Resources\1.62.1\Config\bytesDict.bytes

Lưu ý:
- Không tick ghi đè: tool tạo CommonActions_patched.pkg.bytes để test.
- Tick ghi đè: tool vá trực tiếp CommonActions.pkg.bytes và tạo file .bak.
- bytesDict.bytes không phải raw dictionary để chọn trực tiếp trong zstd.
- Nếu dictionary mặc định không còn khớp, cần gửi CommonActions.pkg.bytes + bytesDict.bytes của bản đó để cập nhật tool.

Command CLI:
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --height 1.5
python patch_aov_camera.py "C:\path\Resources\1.62.1" --height 3 --output "C:\path\CommonActions_patched.pkg.bytes"
