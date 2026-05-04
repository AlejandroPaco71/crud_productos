from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tutorial.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# definicion del modelo Product 
class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f"Name: {self.name}  Price: {self.price}  Stock: {self.stock}"


#funcion para iniciar la base dedatos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos con tabla Product creado exitosamente")


        


if __name__ == "__main__":
    init_db()
