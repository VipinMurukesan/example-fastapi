# import pytest
# from app.calculations import add,subtract,multiply,divide,BankAccount,InsufficientFundsException


# @pytest.fixture
# def zero_bank_account():
#   print("creating empty bank account")
#   return BankAccount()

# @pytest.fixture
# def bank_account():
#   print("creating default bank account")
#   return BankAccount(50)


# def test_bank_set_initial_amount(bank_account):
#   print("test_bank_set_initial_amount")
#   assert bank_account.balance == 50

# def test_bank_default_amount(zero_bank_account):
#   print("test_bank_default_amount")
#   assert zero_bank_account.balance == 0

# def test_bank_withdraw(bank_account):
#     print("test_bank_withdraw")
#     bank_account.withdraw(50)
#     assert bank_account.balance == 0

# def test_bank_deposit(bank_account):
#     print("test_bank_deposit")  
#     bank_account.deposit(50)
#     assert bank_account.balance == 100

# def test_bank_collect_interest(bank_account):
#     print("test_bank_collect_interest") 
#     bank_account.deposit(50)
#     bank_account.collect_intrest()
#     assert round(bank_account.balance,2) == 110


# @pytest.mark.parametrize("deposit,withdraw,expected",
#                          [ (200,100,100),(50,10,40),(1200,200,1000)])
# def test_bank_transaction(zero_bank_account,deposit,withdraw,expected):
#    zero_bank_account.deposit(deposit)
#    zero_bank_account.withdraw(withdraw)
#    assert zero_bank_account.balance == expected    

# def test_insufficient_funds(zero_bank_account):
#    with pytest.raises(InsufficientFundsException):
#       zero_bank_account.withdraw(200)

      



# # @pytest.mark.parametrize("num1,num2,expected",[
# # (3,2,5),(7,1,8),(12,4,16)
# # ])
# # def test_add(num1,num2,expected):
# #   sum = add(num1,num2)
# #   assert sum == expected

# # @pytest.mark.parametrize("num1,num2,expected",[
# #  (3,2,1),(7,1,6),(12,4,8) 
# #  ])
# # def test_subtract(num1,num2,expected):
# #   assert subtract(num1,num2) == expected

# # @pytest.mark.parametrize("num1,num2,expected",[
# #   (3,2,6),(7,1,7),(12,4,48) 
# # ])
# # def test_multiply(num1,num2,expected):
# #   assert multiply(num1,num2) == expected  

# # @pytest.mark.parametrize("num1,num2,expected",[
# #   (3,2,1.5),(7,1,7),(12,4,3) 
# # ])
# # def test_divide(num1,num2,expected):
# #   assert divide(num1,num2) == expected  



 
