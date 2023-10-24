from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client,test_posts):
  res = authorized_client.get("/posts")
  posts = res.json()
  assert len([schemas.PostOut(**post) for post in posts]) == len(test_posts)
  assert res.status_code == 200
  assert len(posts) == len(test_posts)

def test_unauthorized_user_get_all_posts(client,test_posts):
  res = client.get("/posts")
  assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
  res = client.get(f"/posts/{test_posts[0].id}")
  assert res.status_code == 401

def test_authorized_user_get_one_post_not_exist(authorized_client,test_posts):
  res = authorized_client.get("/posts/888888")
  assert res.status_code == 404

@pytest.mark.parametrize("title,content,published",[
  ("awesome new title","awesome new content",True),
  ("favourite pizza","love pepperoni",False),
  ("tallest skyscrapers","wahoo",True)])   
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
  res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
  assert res.status_code == 201

  created_post = schemas.PostReturn(**res.json())
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == published
  assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client,test_user):
  res = authorized_client.post("/posts/",json={"title":"New post","content":"Content for new post"})
  assert res.status_code == 201

  created_post = schemas.PostReturn(**res.json())
  assert created_post.published == True


def test_unauthorized_user_create_post(client,test_user):
    res = client.post("/posts/",json={"title":"New post","content":"Content for new post"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")    
    assert res.status_code == 401    

def test_authorized_user_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")    
    assert res.status_code == 204     

def test_authorized_user_delete_non_exist_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/8888")    
    assert res.status_code == 404

def test_delete_other_users_post(authorized_client,test_user,test_posts):
   post_id = [post for post in test_posts if post.owner_id != test_user['id'] ][0].id
   res = authorized_client.delete(f"/posts/{post_id}")  
   assert res.status_code == 403
   
def test_update_post(authorized_client,test_user,test_posts):
   old_post =  test_posts[0]
   res = authorized_client.put(f"/posts/{old_post.id}",json={"title":"Updated post title","content":"Updated post content"} )
   assert res.status_code == 200 
   updated_post = schemas.PostReturn(**res.json())
   assert updated_post.id == old_post.id
   assert updated_post.title == "Updated post title"
   assert updated_post.content == "Updated post content"
   assert updated_post.published == old_post.published
   assert updated_post.owner_id ==old_post.owner_id

def test_update_other_users_post(authorized_client,test_user,test_posts):
   post_id = [post for post in test_posts if post.owner_id != test_user['id'] ][0].id
   res = authorized_client.put(f"/posts/{post_id}",json={"title":"Updated post title","content":"Updated post content"})  
   assert res.status_code == 403

       
def test_unauthorized_user_update_post(client,test_user,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}",json={"title":"Updated post title","content":"Updated post content"})    
    assert res.status_code == 401 

def test_authorized_user_update_non_exist_post(authorized_client,test_user,test_posts):
       res = authorized_client.put(f"/posts/8888",json={"title":"Updated post title","content":"Updated post content"}) 
       assert res.status_code == 404    