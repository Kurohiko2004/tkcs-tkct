Output sau khi xuất từ md sang csv sẽ chứa các cột sau (trừ PL 4.3):
- STT
- Tên yêu cầu chức năng
- Mô tả yêu cầu chức năng
- Đối tượng sử dụng


Cách mapping dữ liệu từ file md sang csv:
1. File PL 4.3: stt - stt, mô tả yêu cầu - tên yêu cầu chức năng
2. FIle PL 4.4: stt - stt, tên usecase - tên yêu cầu chức năng, tên tác nhân chính - đối tượng sử dụng 
3. FIle PL 4.5: stt - stt, tên chức năng - tên yêu cầu chức năng, tác nhân chính - đối tượng sử dụng, Mô tả chức năng nghiệp vụ - Mô tả yêu cầu chức năng
4. File PL 4.6: bỏ qua
5. File Phụ lục IV (có từ khóa TKCS trong tên file): tìm đến headings "Danh sách các yêu cầu của người sử dụng", trong headings này có bảng danh sách yêu cầu. Map như sau: stt - stt, yêu cầu người sử dụng - Tên yêu cầu chức năng, MÔ TẢ YÊU CẦU NGƯỜI SỬ DỤNG - Mô tả yêu cầu chức năng, đối tượng thực hiện - Đối tượng sử dụng