from flask import Flask, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("best.pt")  # 加载模型

# 定义一个字典来映射英文类别名到中文描述
category_map = {
    "good": "井盖完好",
    "broke": "井盖破损",
    "lose": "井盖缺失",
    "uncovered": "井盖未盖",
    "circle": "井圈问题"
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件被上传"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "没有文件被上传"}), 400
    
    # 保存上传的文件到临时文件中
    file_path = "/tmp/uploaded_image.png"
    file.save(file_path)
    
    # 对图片进行预测
    results = model.predict(source=file_path)
    
    # 准备结果
    predictions = []
    for result in results:
        class_ids = result.boxes.cls
        for cls_id in class_ids:
            class_name = model.names[int(cls_id)]
            chinese_name = category_map[class_name]
            predictions.append(chinese_name)
    
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
