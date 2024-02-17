from jardiquest.model.database.entity.user import *


def test_user_validation():
    assert type(User.is_valid_commit('', '', '')) is not bool
    assert type(User.is_valid_commit('invalidmail', 'name', 'password')) is not bool
    assert type(User.is_valid_commit('mail@mail.com', '', 'password')) is not bool
    assert type(User.is_valid_commit('mail@mail.com', 'name', 'password')) is bool
    assert type(User.is_valid_commit('mail@mail.com', 'name', 'short')) is not bool
