import pytest
from app import models

def test_vote_on_post(authorized_client,test_posts,test_user):
  post_id = [post for post in test_posts if post.owner_id != test_user['id'] ][0].id
  res = authorized_client.post("/votes",json={"post_id":post_id,"dir":1})
  assert res.status_code == 201 
  assert res.json()['message'] == "successfully added vote"

@pytest.fixture
def test_vote(test_posts,test_user,session):
  post_id = [post for post in test_posts if post.owner_id != test_user['id'] ][0].id
  vote = models.Vote(post_id = post_id,user_id = test_user['id'])
  session.add(vote)
  session.commit()
  return {"id":post_id}


def test_vote_on_post_twice(authorized_client,test_posts,test_user,test_vote):
  post_id = test_vote['id']
  res = authorized_client.post("/votes",json={"post_id":post_id,"dir":1})
  assert res.status_code == 409 
  assert res.json()['detail'] == f"user {test_user['id']} has already voted on post id {post_id}"


def test_delete_vote(authorized_client,test_posts,test_user,test_vote):
  post_id = test_vote['id']
  res = authorized_client.post("/votes",json={"post_id":post_id,"dir":0})
  assert res.status_code == 201 
  assert res.json()['message'] == "vote has been removed"


  def test_delete_vote_not_exist(authorized_client,test_posts,test_user):     
    post_id = [post for post in test_posts if post.owner_id != test_user['id'] ][0].id
    res = authorized_client.post("/votes",json={"post_id":post_id,"dir":0})
    assert res.status_code == 404
    assert res.json()['detail'] == "vote does not exist"


def test_authorized_user_vote_non_exist_post(authorized_client,test_user,test_posts):
    res = authorized_client.post("/votes",json={"post_id":8888,"dir":0})  
    assert res.status_code == 404
    assert res.json()['detail'] == f"post with post id 8888 cannot be found"

@pytest.mark.parametrize("dir",[(1,),(0,)])
def test_vote_own_post(authorized_client,test_user,test_posts,dir):
   post_id = [post for post in test_posts if post.owner_id == test_user['id'] ][0].id
   res = authorized_client.post("/votes",json={"post_id":post_id,"dir":1})    
   assert res.status_code == 409
   assert res.json()['detail'] == f"user {test_user['id']} cannnot vote on post id {post_id} created by {test_user['id']}"

@pytest.mark.parametrize("dir",[(1,),(0,)])
def test_unauthorized_user_vote(client,test_user,test_posts,dir):
    post_id = [post for post in test_posts if post.owner_id == test_user['id'] ][0].id
    res = client.post("/votes",json={"post_id":post_id,"dir":1})    
    assert res.status_code == 401
