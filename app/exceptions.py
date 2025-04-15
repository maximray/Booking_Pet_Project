from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self): 
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):

    status_code=status.HTTP_409_CONFLICT
    detail="User already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Incorrect Email or password'


class TokenExpireException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token has expired'


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token missing'


class IncorrectFormatTokenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Invalid token format'


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail = 'No rooms left'


class NoHotelByID(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail = 'No hotel by id'

class IncorrectDate(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail = 'Incorrect date_from and date_to'
    