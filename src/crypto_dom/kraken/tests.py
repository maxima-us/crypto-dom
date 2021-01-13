import hypothesis
import pydantic

from requests import _OhlcReq, _OhlcResp, T_OhlcResp


generictype = T_OhlcResp["XXBTZUSD"]

test = _OhlcResp("XXBTZUSD")


data1 = {
    "XXBTZUSD":[
       [1607947200,"19100.8","19123.7","19025.1","19108.2","19076.7","88.36173782",671],
       [1607950800,"19108.2","19195.2","19062.4","19174.3","19151.0","117.93370323",704],
       [1607954400,"19174.4","19215.4","19099.9","19215.4","19153.3","163.81512930",753]],
    "last":"number"
}

data2 = {
    "XXBTZUSD":[
       [1607947200,"19100.8","19123.7","19025.1","19108.2","19076.7","88.36173782",671],
       [1607950800,"19108.2","19195.2","19062.4","19174.3","19151.0","117.93370323",704],
       [1607954400,"19174.4","19215.4","19099.9","19215.4","19153.3","163.81512930",753]],
    "last": 123014050535
}

# should be fine
print("\nFirst call", test(**data2))

# should throw error
# print("\nSecond call", test(**data1))



class User(pydantic.BaseModel):

    name: pydantic.StrictStr
    age: int
    city: str


@hypothesis.given(hypothesis.strategies.from_type(User))
def test_me(person: User):
    user = User(
        name="maximaus",
        age=person.age,
        city=person.city
    )
    assert user.age < 330
    assert isinstance(user, User)


#!!!! constrained types dont work properly, see: https://github.com/samuelcolvin/pydantic/pull/2097#issuecomment-748596129
@hypothesis.given(hypothesis.strategies.from_type(_OhlcReq))
def test_request(generated: _OhlcReq):

    print (generated)

    request = _OhlcReq(
        pair=generated.pair,
        interval=generated.interval,
        #! since there is no way to test this for now we will leave it at 1
        #! == still doesnt work
        since=1
    )

    assert isinstance(request, _OhlcReq)

test_request()

