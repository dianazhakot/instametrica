from django.contrib import messages
from django.shortcuts import render, redirect
from igramscraper.instagram import Instagram

instagram = Instagram()


def home(request):
    if request.method == 'POST':
        try:
            url = request.POST['url']
            media = instagram.get_media_by_url(url)
            likes_count = media.likes_count
            caption = media.caption
            username = media.owner.username
            account = instagram.get_account(username)
            comments = instagram.get_media_comments_by_id(media.identifier, 300)
            comments = len(comments["comments"])
            profile_picture = account.profile_pic_url_hd
            hashtag_count = 0
            tags_list = []
            is_video = False
            is_many_likes = False
            is_many_followers = False
            has_more_comments = False
            popular_tags = False
            followers = account.followed_by_count
            # is video Check
            if media.type == 'video':
                is_video = True
                media_photo = media.video_standard_resolution_url
            else:
                media_photo = media.image_high_resolution_url
            # Likes Check
            if likes_count > 200:
                is_many_likes = True
            # Hashtags popularity Check
            if caption is not None:
                tags_list = caption.split("#")
                if len(tags_list) > 1:
                    caption = tags_list.pop(0)
                    hashtag_count = len(tags_list)
                    if hashtag_count > 10:
                        popular_tags = True
                    else:
                        tags_popolar_counter = 0
                        for tag in tags_list:
                            popular_counter = 0
                            medias = instagram.get_current_top_medias_by_tag_name(tag)
                            for media in medias:
                                if media.likes_count > 150:
                                    popular_counter += 1
                            if popular_counter >= 6:
                                tags_popolar_counter += 1
                        if tags_popolar_counter >= hashtag_count * 0.5:
                            popular_tags = True
                else:
                    tags_list = None
            # Followers Check
            if followers > 400:
                is_many_followers = True
            # Comments Check
            if comments > 15:
                has_more_comments = True
            context = {
                'likes': likes_count,
                'comments': comments,
                'hashtags': hashtag_count,
                'username': username,
                'followers': followers,
                'caption': caption,
                'has_more_comments': has_more_comments,
                'popolar_tags': popular_tags,
                'is_many_followers': is_many_followers,
                'source': media_photo,
                'is_many_likes': is_many_likes,
                'tags_list': tags_list,
                'is_video': is_video,
                'profile_picture': profile_picture

            }
            return render(request, 'instametric/post-info.html', context=context)
        except BaseException as e:
            print(e)
            return redirect('page-not-found')
    return render(request, 'instametric/home.html')


def postinfo(request):
    return render(request, 'instametric/post-info.html')


def page_not_found(request):
    return render(request, 'instametric/404.html')
