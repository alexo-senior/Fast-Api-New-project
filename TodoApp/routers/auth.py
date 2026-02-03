from fastapi import APIRouter # dara la ruta de main.py a auth.py 


router = APIRouter()


# ahora con el router es una ruta en lugar de una app

@router.get("/auth")
async def get_user():
    return {'user':'authenticated'}
