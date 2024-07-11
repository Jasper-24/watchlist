from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/todolist_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    used = db.Column(db.Boolean, default=False)

class AchievementPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_points = db.Column(db.Integer, nullable=False)

# 创建数据库
@app.before_request
def create_tables():
    db.create_all()

# 获取所有任务
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'name': task.name, 'points': task.points, 'completed': task.completed} for task in tasks])

# 主页路由
@app.route('/')
def home():
    tasks = Task.query.all()  # 获取所有任务数据
    return render_template('home.html', tasks=tasks)  # 将任务数据传递给模板


# 创建新任务
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(name=data['name'], points=data['points'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'name': new_task.name, 'points': new_task.points, 'completed': new_task.completed})

# 更新任务
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.json
        task.name = data.get('name', task.name)
        task.points = data.get('points', task.points)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        update_achievement_points()
        return jsonify({'id': task.id, 'name': task.name, 'points': task.points, 'completed': task.completed})
    return jsonify({'message': 'Task not found'}), 404

# 删除任务
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        update_achievement_points()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'}), 404

# 获取所有奖励
@app.route('/rewards', methods=['GET'])
def get_rewards():
    rewards = Reward.query.all()
    return jsonify([{'id': reward.id, 'name': reward.name, 'points': reward.points, 'used': reward.used} for reward in rewards])

# 创建新奖励
@app.route('/rewards', methods=['POST'])
def add_reward():
    data = request.json
    new_reward = Reward(name=data['name'], points=data['points'])
    db.session.add(new_reward)
    db.session.commit()
    return jsonify({'id': new_reward.id, 'name': new_reward.name, 'points': new_reward.points, 'used': new_reward.used})

# 更新奖励
@app.route('/rewards/<int:id>', methods=['PUT'])
def update_reward(id):
    reward = Reward.query.get(id)
    if reward:
        data = request.json
        reward.name = data.get('name', reward.name)
        reward.points = data.get('points', reward.points)
        reward.used = data.get('used', reward.used)
        db.session.commit()
        update_achievement_points()
        return jsonify({'id': reward.id, 'name': reward.name, 'points': reward.points, 'used': reward.used})
    return jsonify({'message': 'Reward not found'}), 404

# 删除奖励
@app.route('/rewards/<int:id>', methods=['DELETE'])
def delete_reward(id):
    reward = Reward.query.get(id)
    if reward:
        db.session.delete(reward)
        db.session.commit()
        update_achievement_points()
        return jsonify({'message': 'Reward deleted'})
    return jsonify({'message': 'Reward not found'}), 404

# 获取当前成就点数
@app.route('/points', methods=['GET'])
def get_points():
    points = AchievementPoints.query.first()
    if points:
        return jsonify({'total_points': points.total_points})
    return jsonify({'total_points': 0})

# 更新成就点数
def update_achievement_points():
    points = AchievementPoints.query.first()
    if not points:
        points = AchievementPoints(total_points=0)
        db.session.add(points)

    total_points = 0
    tasks = Task.query.all()
    rewards = Reward.query.all()

    for task in tasks:
        if task.completed:
            total_points += task.points

    for reward in rewards:
        if reward.used:
            total_points -= reward.points

    points.total_points = total_points
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
