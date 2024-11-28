import os
from flask import Flask, render_template, jsonify
import psycopg2
import redis
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)

# Database Connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        database='monitoring_db',
        user='admin',
        password='secret_password'
    )

# Redis Connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

# Kafka Consumer Thread
def kafka_consumer_thread():
    consumer = KafkaConsumer(
        'monitoring_server.public.user_activities',
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        auto_offset_reset='earliest',
        group_id='flask-dashboard-consumer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        # Process Debezium change events
        change_event = message.value
        if change_event['payload']['op'] in ['c', 'u', 'd']:
            # Cache recent changes in Redis
            redis_client.lpush('recent_changes', json.dumps(change_event))
            redis_client.ltrim('recent_changes', 0, 99)  # Keep last 100 changes

@app.route('/')
def dashboard():
    # Fetch recent database activities
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_activities ORDER BY timestamp DESC LIMIT 50")
    activities = cur.fetchall()
    cur.close()
    conn.close()

    # Retrieve cached changes from Redis
    recent_changes = [json.loads(change) for change in redis_client.lrange('recent_changes', 0, -1)]

    return render_template('dashboard.html', 
                           activities=activities, 
                           recent_changes=recent_changes)

@app.route('/metrics')
def metrics():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Sample metrics queries
    cur.execute("SELECT activity_type, COUNT(*) as count FROM user_activities GROUP BY activity_type")
    activity_metrics = cur.fetchall()
    
    cur.close()
    conn.close()

    return jsonify({
        'activity_metrics': dict(activity_metrics)
    })

if __name__ == '__main__':
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer_thread)
    consumer_thread.start()

    app.run(host='0.0.0.0', port=5000)