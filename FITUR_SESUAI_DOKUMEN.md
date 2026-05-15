# Pemetaan Fitur Terhadap Spesifikasi Dokumen

Dokumen meminta aplikasi Mini Photoshop berbasis Python untuk mata kuliah Pengolahan Citra Digital. Versi **Mini Photoshop Pro** memenuhi spesifikasi tersebut dengan UI yang lebih jelas, live preview, dan parameter fleksibel.

| Spesifikasi Dokumen | Implementasi di Program |
|---|---|
| Load image JPG/PNG/BMP | Tombol **Load**, menu File > Load Image |
| Save image custom filename & format | Tombol **Save**, menu File > Save Result, dukungan PNG/JPEG/BMP/TIFF |
| Reset ke gambar awal | Tombol **Reset**, menu File > Reset |
| Preview before-after | Dua canvas: **Before** dan **After / Live Result** |
| Brightness & contrast slider | Fitur **Brightness & Contrast** dengan live slider |
| Histogram equalization | Fitur **Histogram Equalization** |
| Sharpening | Fitur **Sharpening Fleksibel** dengan strength, kernel, sigma |
| Smoothing blur | Fitur **Smoothing / Average Blur** dengan kernel size |
| Rotate 0-360 | Fitur **Rotate / Scale / Translate** |
| Flip horizontal/vertical | Fitur **Flip Horizontal** dan **Flip Vertical** |
| Crop drag area | Drag pada panel After, lalu klik **Crop Area** |
| Resize/scaling | Fitur **Resize / Scaling** berdasarkan persentase width/height |
| Translation | Parameter Translate X/Y pada fitur affine transform |
| Matrix affine | Diimplementasikan pada `ip.affine_transform()` memakai OpenCV affine matrix |
| Interpolation nearest/bilinear | Combobox **Interpolasi Transform** |
| Gaussian blur | Fitur **Gaussian Blur** dengan kernel dan sigma |
| Median filter | Fitur **Median Filter** |
| Salt & pepper removal | Fitur **Salt & Pepper Removal** |
| Thresholding binary | Fitur **Threshold Binary** dengan invert option |
| Canny edge | Fitur **Edge Detection Lengkap** metode Canny, low/high threshold |
| Sobel, Prewitt, Robert | Metode tersedia di **Edge Detection Lengkap** |
| Laplacian dan LoG | Metode tersedia di **Edge Detection Lengkap** |
| Morphology erosion/dilation | Fitur **Morphology Erosion/Dilation** dengan kernel dan iterations |
| RGB ke grayscale | Fitur **RGB → Grayscale** |
| Channel splitting R/G/B | Fitur **Channel Splitting RGB** |
| Hue/saturation | Fitur **Hue / Saturation** |
| Threshold-based segmentation | Fitur **Threshold Segmentation** |
| Edge-based segmentation | Fitur **Edge-based Segmentation** |
| Region-based sederhana | Fitur **Region-based / K-Means** |
| JPEG compression simulation | Fitur **Simulasi JPEG Quality** |
| Quantization | Fitur **Color Quantization** |
| RLE | Fitur **RLE Compression Ratio** |
| Histogram grayscale/RGB | Tombol **Histogram** menampilkan before-after histogram grayscale dan RGB |
| Menu toolbar | Toolbar atas dan menu File/Edit/View/Help |
| Slider parameter | Panel kanan **Parameter Fleksibel** |
| Tombol aksi cepat | Sidebar **Aksi Cepat** dan toolbar atas |
| CNN sebagai nilai tambah | Tombol **CNN** dan fitur **CNN Object Recognition** opsional |

## Peningkatan Tambahan

- UI 3 kolom agar fitur mudah ditemukan.
- Parameter muncul sesuai fitur yang dipilih.
- Preset Ringan/Sedang/Kuat untuk fitur yang memiliki intensitas.
- Live preview ON/OFF.
- Apply/Cancel agar pengguna bisa mencoba efek sebelum menyimpan state edit.
- Undo/Redo bertingkat.
- Status bar berisi informasi ukuran gambar dan proses aktif.
