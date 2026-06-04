from fastapi import APIRouter

from src.days_6.days6 import ML

mlRouter = APIRouter()

ml = ML()
df = ml.load_csv()

# predict_top_spenders_next_30_days endpoint
@mlRouter.get("/30gunHarcamaYapacaklar")
def predict_top_spenders_next_30_days():
    top_spenders = ml.predict_top_spenders_next_30_days(df)
    return {
        "success": True,
        "data": top_spenders.to_dict(orient="records")
    }