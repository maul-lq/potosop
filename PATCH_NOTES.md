# Patch Notes

## Perbaikan CNN Prediction Format

Masalah:
- Tombol CNN/Object Recognition crash dengan error: `TypeError: cannot unpack non-iterable Prediction object`.
- Penyebabnya UI membaca hasil prediksi sebagai tuple `(label, score)`, sedangkan modul `ml.py` mengembalikan objek `Prediction(label, confidence)`.

Perbaikan:
- Menambahkan fungsi `prediction_to_label_score()` agar UI menerima format:
  - `Prediction(label, confidence)`
  - `(label, score)`
  - format Keras/ImageNet `(class_id, label, score)`
- Menambahkan `format_predictions()` untuk membuat pesan hasil CNN secara aman.
- Menambahkan test `tests/test_cnn_prediction_format.py`.

Cara pakai:
1. Ekstrak ZIP.
2. Jalankan `pip install -r requirements.txt`.
3. Untuk CNN, jalankan `pip install -r requirements-ml.txt`.
4. Jalankan `python main.py`.
