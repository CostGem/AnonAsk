# Russian dictionary

# Message text
welcome_message =
    👋 Welcome to the First School news bot!
    This bot will help you find out all the latest information about upcoming events and innovations, including changes in the schedule. The uniqueness of the bot is that you can anonymously comment on posts in the channel, expressing your opinion in order to provide constructive criticism.

    📝 Before you start using it, you need to register and choose a pseudonym that will be assigned to your account in order to remain incognito.

    📃 Do not forget to follow the rules that are enshrined in the channel description.

    ✨ Convenient use!

start_message = 👋 Welcome to the First School news bot!

back_to_main_message = ◀️ Main menu

profile_message =
    📔 <b>ID:</b> { $user_id }
    📋 <b>Nickname:</b> { $nickname }

    🌀 <b>Role:</b> { $role_name }
    💠 <b>Status:</b> { $status_emoji }

    { $locale_emoji } <b>Language:</b> { $locale_name }

    📆 <b>Registration date:</b> { $register_date }

set_nickname_message = 📋 Enter the nickname under which you will be visible to other users

nickname_is_taken_message = ‼️ This nickname is already taken. Enter another

nickname_length_to_long_message = ‼️ The maximum length of a nickname can be 12 characters

nickname_setting_message = 📋 Your nickname has been changed to "{ $nickname }"

post_not_found_message = ‼️ Post to comment was not found

comment_to_reply_not_found_message = ‼️ Comment to reply not found

attachments_are_not_supported_message =
    ‼️ You can only send text, photo, video or sticker!

send_comment_to_post_message = ✉️ Send your comment to { $post_link }post</a>

send_reply_comment_message =
    ✉️ Submit your response to this { $comment_link }comment</a>

cancel_commenting_message = ‼️ You have canceled commenting

can_only_attach_one_attachment_message = ‼️ You can only attach one attachment

you_can_not_block_an_admin_message = ‼️ You cannot block the administrator

you_can_not_delete_an_admin_message = ‼️ You cannot delete an admin comment

post_message =
    { $have_text ->
    [1] { $post_text }

    ✍️ <b>{ $comment_post_url }Comment on post</a></b> ✍️
    *[0] ✍️ <b>{ $comment_post_url }Comment on post</a></b> ✍️
    }

comment_message =
    { $status_emoji } "{ $nickname }"

    { $have_text ->
    [1]
    { $user_message }

    <b>{ $reply_to_comment_url }💭 Reply 💭</a></b>
    *[0]
    <b>{ $reply_to_comment_url }💭 Reply 💭</a></b>
    }

comment_sent_successfully_message =
    ✅ Your comment to { $post_url }post</a> was successfully left

    🔖 Link to comment: { $comment_url }

commenting_cooldown_message =
    ‼️ You can comment on a post and reply to other users once every 30 seconds

reply_to_comment_sent_successfully_message =
    ✅ Your reply to { $comment_url }comment</a> was successfully left

    🔖 Link to reply: <b>{ $reply_url }</b>

user_reply_to_our_comment_message =
    💭 User "{ $nickname }" { $reply_url }replied</a> to your { $comment_url }comment</a>

file_info_message =
    🖼 Attachment information:

    📋 <b>ID:</b>
    { $file_id }

    🏞 <b>Resolution:</b> { $height }x{ $width }

    💾 <b>Weight:</b>
    { $file_size }

timetable_message =
    📅 <b>Lesson schedule on { $is_today_timetable ->


    [1] { $prev_lessons_date }

    {$lessons}

    👇 You can see the schedule on { $next_lessons_date }
    *[0] { $next_lessons_date }

    {$lessons}

    👇 You can see the schedule on { $prev_lessons_date }
    } by clicking the button below</b>

timetable_not_found =
    📅 Schedule for { $is_today_selected ->
    [1] { $today_date } not published yet

    🗓 Try looking at the schedule for { $tomorrow_date }
    *[0] { $tomorrow_date } not published yet

    🗓 Try looking at the schedule for { $today_date }
    }

send_timetable_photo_message = 🗓 Send a photo of your timetable

choose_timetable_date_message = 📅 Select the date you want to add a schedule for

choose_timetable_schedule_message = 🔔 Select call schedule

timetable_add_confirmation_message =
    📅 <b>Schedule date:</b> { $target_date }

    <b>{ $lessons }</b>

    ⁉️ <b>Are you sure you want { $is_changing_timetable ->
    [1] change existing
    *[0] add new
    } schedule?</b>

confirm_timetable_add_message =
    ✅ <b>Schedule on { $target_date } successfully { $is_changing_timetable ->
    [1] changed
    *[0] added
    }</b>

cancel_timetable_add_message =
    ‼️ <b>{ $is_changing_timetable ->
    [1] Change
    *[0] Addition
    } schedules cancelled</b>

mailing_started_message = ‼️ <b>The mailing has started...</b>

mailing_statistics_message =
    ✅ <b>Messages sent:</b> { $success_messages_count }

    ❌ <b>Bot blocked:</b> { $fail_messages_count }

mailing_end_message =
    🎉 <b>Mailing completed</b>

    ✅ <b>Messages sent:</b> { $success_messages_count }

    ❌ <b>Bot blocked:</b> { $fail_messages_count }

timetable_added_message =
    📅 Schedule on <b>{ $target_date }</b> { $is_changing_timetable ->
    [1] has been changed
    *[0] added
    }!

locales_list_message = ‼️ Select interface language

same_locale_selected_message = { $emoji } You cannot select the language you have installed

locale_changed_message = { $emoji } The interface language has been changed to <b>"{ $name }"</b>

links_are_prohibited_message = ‼️ Links and mentions are prohibited in the text

emoji_are_prohibited_in_nickname_message = ‼️ Emoji are prohibited in nickname

its_not_comment_message = ‼️ This forwarded message is not a comment

comment_not_found_message = ‼️ Comment not found

comments_deleted_message =
    ‼️ User comment and replies to it have been deleted

    💭 Comment ID: { $comment_id }

comments_deleted_and_user_banned_message =
    ‼️ The user is blocked. The comment and its replies have been deleted

    💭 Comment ID: { $comment_id }

your_comment_has_been_deleted_message =
    ‼️ Your comment has been deleted. We advise you to read our rules in order to avoid blocking

    💭 Comment ID: { $comment_id }

    📑 Rules -> <b>https://teletype.in/@neqox/news_sosh1_rules</b>

you_have_been_blocked =
    ‼️ You have been blocked by the administrator and can no longer comment on posts in our channel

    💭 Comment ID: { $comment_id }

    📑 If you think the blocking is unfair, please contact -> <b>@neqox</b>

you_blocked =
    ‼️ You have been blocked by the administrator and can no longer comment on posts in our channel

    📑 If you think the blocking is unfair, please contact -> <b>@neqox</b>

comment_user_info_message =
    💭 <b>Comment from “{ $nickname }”</b>
    📖 <b>Name:</b> { $name }
    📋 <b>Tag:</b> { $username }
    🌀 <b>Role:</b> { $role_name }
    💠 <b>Status:</b> { $status_emoji }

today_timetable_not_found_message = ‼️ No schedule found for today

user_achievements_message =
    🏵 <b>Your achievements:</b>

    { $achievements }

    <b>To find out more about the achievement, click the corresponding button with the number</b> 👇

you_have_not_achievements_message = 🏵 <b>You currently have no achievements</b>

achievement_details_message =
    🏵 <b>Achievement:
    "{ $achievement_name }"</b>

    <i>{ $achievement_description }</i>

    🎖 <b>Reward:</b> { $status_emoji }

user_statuses_message = 💠 Select the status that will be displayed in the comments

status_not_found_message = ‼️ Status not found

achievement_property_not_found_message = ‼️ The code for obtaining the achievement was not found

user_have_achievement_message = ‼️ The user already has this achievement

user_activated_achievement_message = ‼️ You have already received the achievement via this link

achievement_activation_from_date_message = ‼️ The time to receive the achievement has not yet come

achievement_activation_until_date_message = ‼️ The time to get the achievement has passed

achievement_activated_success_message =
    🏵 You have received the achievement <b>“{ $achievement_name }”</b>

    💠 <b>New status opened:</b> { $status_emoji }

# Button text
nickname_button_text =
    { $is_changing ->
    [1] 📋 Change nickname
    *[0] 📋 Select nickname
    }

achievements_button_text = 🏵 Achievements

statuses_button_text = 💠 Statuses

timetable_button_text = 📚 Schedule

profile_button_text = 📝 Profile

back_to_main_button_text = ◀️ To main menu

cancel_commenting_button_text = ❌ Cancel commenting

confirm_timetable_add_button_text = ✅ Confirm

cancel_timetable_add_button_text = ❌ Cancel

back_button_text = ◀️ Back

locales_list_button_text =
    { $emoji } { $name } { $is_user_locale ->
    [1] ✅
    *[0]ㅤ
    }

statuses_list_button_text =
    { $is_user_status ->
    [1] { $emoji } ✅
    *[0] { $emoji }
    }

timetable_list_button_text =
    { $target_date } { $is_current ->
    [1] ✅
    *[0]ㅤ
    }

change_locale_button_text = 🌎 Change language

delete_comment_button_text = ❌ Delete comment

ban_comment_user_button_text = 🚫 Block

# Command descriptions
start_command_description = 👑 Start

timetable_command_description = 🗓 Add schedule