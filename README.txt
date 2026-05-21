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
1. Mở Mod_Camera_Lien_Quan.exe.
2. Chọn CommonActions.pkg.bytes hoặc file bị đổi tên kiểu CommonActions.pkg_1.bytes, hoặc chọn thư mục Ages/Resources.
3. Chọn kgvn.app hoặc kgvn.app\Data\resources.assets của đúng bản game update.
4. Chọn nơi lưu file đã mod. File kết quả nên giữ đúng tên CommonActions.pkg.bytes.
5. Chọn mức camera 10%, 20% hoặc 40%, rồi bấm Mod ngay.

Đường dẫn lấy CommonActions trong game:
Documents\Resources\1.62.1\Ages\Prefab_Characters\Prefab_Hero\CommonActions.pkg.bytes

Đường dẫn lấy raw dictionary trong IPA/app:
kgvn.app\Data\resources.assets

Lưu ý:
- Không tick ghi đè: tool tạo CommonActions_mod\CommonActions.pkg.bytes để test.
- Tick ghi đè: tool vá trực tiếp CommonActions.pkg.bytes và tạo file .bak.
- Tool tự đọc dict id trong CommonActions, quét resources.assets và dò đúng raw zstd dictionary.
- Tool không dùng zstd_dict.bin mặc định cũ, tránh lỗi lấy nhầm dictionary của bản cũ.

Command CLI:
python patch_aov_camera.py "C:\path\CommonActions.pkg.bytes" --game-assets "C:\path\kgvn.app" --height 1.5 --output "C:\path\CommonActions_mod\CommonActions.pkg.bytes"
