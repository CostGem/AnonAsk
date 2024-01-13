# Русский словарь

# Текста сообщений
welcome_message =
    <b>👋 Приветствуем в новостном боте Первой школы!
    Этот бот поможет Вам узнавать всю актуальную информацию о предстоящих событиях и нововведениях, включая изменения в расписании. Уникальность бота состоит в том, что Вы сможете анонимно комментировать посты в канале, высказывая своё мнение с целью внести конструктивную критику.

    📝 Чтобы комментировать посты, вас необхожимо выбрать псевдоним, который закрепится за Вашим аккаунтом, чтобы оставаться инкогнито.

    📃 Не забывайте о соблюдении правил, которые закреплены в описании канала.

    ✨ Удобного пользования!</b>

back_to_main_message = ◀️ Главное меню

profile_message =
    📔 <b>ID:</b> { $user_id }
    📋 <b>Никнейм:</b> { $have_nickname ->
        [1] { $nickname }
        *[0] Не указан
        }

    🌀 <b>Роль:</b> { $role_name }
    💠 <b>Статус:</b> { $status_emoji }

    { $locale_emoji } <b>Язык:</b> { $locale_name }

    📆 <b>Дата регистрации:</b> { $register_date }

set_nickname_message = 📋 Введите псевдоним, под которым вы будете видны другим пользователям

nickname_is_taken_message = ‼️ Данный никнейм уже занят. Введите другой

nickname_length_to_long_message = ‼️ Максимальная длина никнейма может составлять 12 символов

nickname_setting_message = 📋 Ваш никнейм изменён на "{ $nickname }"

post_not_found_message = ‼️ Запись для комментирования не найдена

comment_to_reply_not_found_message = ‼️ Комментарий для ответа не найден

attachments_are_not_supported_message =
    ‼️ Вы можете отправлять только текст, фото, видео или стикер!

send_comment_to_post_message = ✉️ Отправьте ваш комментарий к { $post_link }записи</a>

send_reply_comment_message =
    ✉️ Отправьте ваш ответ на этот { $comment_link }комментарий</a>

cancel_commenting_message = ‼️ Вы отменили комментирование

can_only_attach_one_attachment_message = ‼️ Вы можете прикрепить только одно вложение

you_can_not_block_an_admin_message = ‼️ Вы не можете заблокировать администратора

you_can_not_delete_an_admin_message = ‼️ Вы не можете удалить комментарий администратора

post_message =
    { $have_text ->
    [1] { $post_text }

    ✍️ <b>{ $comment_post_url }Комментировать запись</a></b> ✍️
    *[0] ✍️ <b>{ $comment_post_url }Комментировать запись</a></b> ✍️
    }

comment_message =
    { $status_emoji } «{ $nickname }»

    { $have_text ->
    [1]
    { $user_message }

    <b>{ $reply_to_comment_url }💭 Ответить 💭</a></b>
    *[0]
    <b>{ $reply_to_comment_url }💭 Ответить 💭</a></b>
    }

comment_sent_successfully_message =
    ✅ Ваш комментарий к { $post_url }записи</a> успешно оставлен

    🔖 Ссылка на комментарий: { $comment_url }

commenting_cooldown_message =
    ‼️ Комментировать запись и отвечать другим пользователям можно раз в 30 секунд

reply_to_comment_sent_successfully_message =
    ✅ Ваш ответ к { $comment_url }комментарию</a> успешно оставлен

    🔖 Ссылка на ответ: <b>{ $reply_url }</b>

user_reply_to_our_comment_message =
    💭 Пользователь «{ $nickname }» { $reply_url }ответил</a> на ваш { $comment_url }комментарий</a>

file_info_message =
    🖼 Информация о вложении:

    📋 <b>ID:</b>
    { $file_id }

    🏞 <b>Разрешение:</b> { $height }x{ $width }

    💾 <b>Вес:</b>
    { $file_size }

timetable_message =
    📅 <b>Расписание уроков на { $is_today_timetable ->


    [1] { $prev_lessons_date }

    { $lessons }

    👇 Вы можете посмотреть расписание на { $next_lessons_date }
    *[0] { $next_lessons_date }

    { $lessons }

    👇 Вы можете посмотреть расписание на { $prev_lessons_date }
    }, нажав кнопку ниже</b>

timetable_not_found =
    📅 Расписание за { $is_today_selected ->
    [1] { $today_date } ещё не опубликовано

    🗓 Попробуйте посмотреть расписание за { $tomorrow_date }
    *[0] { $tomorrow_date } ещё не опубликовано

    🗓 Попробуйте посмотреть расписание за { $today_date }
    }

send_timetable_photo_message = 🗓 Отправьте фотографию расписания

choose_timetable_date_message = 📅 Выберите дату, на которую хотите добавить расписание

choose_timetable_schedule_message = 🔔 Выберите расписание звонков

timetable_add_confirmation_message =
    📅 <b>Дата расписания:</b> { $target_date }

    <b>{ $lessons }</b>

    ⁉️ <b>Вы уверены, что хотите { $is_changing_timetable ->
    [1] изменить существующее
    *[0] добавить новое
    } расписание?</b>

confirm_timetable_add_message =
    ✅ <b>Расписание на { $target_date } успешно { $is_changing_timetable ->
    [1] измено
    *[0] добавлено
    }</b>

cancel_timetable_add_message =
    ‼️ <b>{ $is_changing_timetable ->
    [1] Изменение
    *[0] Добавление
    } расписания отменено</b>

mailing_started_message = ‼️ <b>Рассылка началась...</b>

mailing_statistics_message =
    ✅ <b>Сообщений отправлено:</b> { $success_messages_count }

    ❌ <b>Бота заблокировало:</b> { $fail_messages_count }

mailing_end_message =
    🎉 <b>Рассылка завершена</b>

    ✅ <b>Сообщений отправлено:</b> { $success_messages_count }

    ❌ <b>Бота заблокировало:</b> { $fail_messages_count }

timetable_added_message =
    📅 Расписание на <b>{ $target_date }</b> { $is_changing_timetable ->
    [1] было изменено
    *[0] добавлено
    }!

locales_list_message = ‼️ Выберите язык интерфейса

same_locale_selected_message = { $emoji } Вы не можете выбрать язык, который у вас установлен

locale_changed_message = { $emoji } Язык интерфейса был изменён на <b>"{ $name }"</b>

links_are_prohibited_message = ‼️ В тексте запрещены ссылки и упоминания

emoji_are_prohibited_in_nickname_message = ‼️ Эмоджи запрещены в никнейме

its_not_comment_message = ‼️ Это пересланное сообщение не является комментарием

comment_not_found_message = ‼️ Комментарий не найден

comments_deleted_message =
    ‼️ Комментарий пользователя и ответы на него удалены

    💭 ID комментария: { $comment_id }

comments_deleted_and_user_banned_message =
    ‼️ Пользователь заблокирован. Комментарий и ответы на него удалены

    💭 ID комментария: { $comment_id }

your_comment_has_been_deleted_message =
    ‼️ Ваш комментарий был удалён. Советуем прочитать наши правила, дабы избежать блокировки

    💭 ID комментария: { $comment_id }

    📑 Правила -> <b>https://teletype.in/@neqox/news_sosh1_rules</b>

you_have_been_blocked =
    ‼️ Вы были заблокированы администратором и больше не можете комментировать записи в нашем канале

    💭 ID комментария: { $comment_id }

    📑 Если вы считаете, что блокировка несправедлива, обратитесь -> <b>@neqox</b>

you_blocked =
    ‼️ Вы были заблокированы администратором и больше не можете комментировать записи в нашем канале

    📑 Если вы считаете, что блокировка несправедлива, обратитесь -> <b>@neqox</b>

comment_user_info_message =
    💭 <b>Комментарий от «{ $nickname }»</b>
    📖 <b>Имя:</b> { $name }
    📋 <b>Тег:</b> { $username }
    🌀 <b>Роль:</b> { $role_name }
    💠 <b>Статус:</b> { $status_emoji }

today_timetable_not_found_message = ‼️ Расписание на сегодня не найдено

user_achievements_message =
    🏵 <b>Ваши достижения:</b>

    { $achievements }

    <b>Чтобы узнать подробнее о достижении, нажмите соответствующую кнопку с номером</b> 👇

you_have_not_achievements_message = 🏵 <b>На данный момент у вас нет достижений</b>

achievement_details_message =
    🏵 <b>Достижение:
    «{ $achievement_name }»</b>

    <i>{ $achievement_description }</i>

    🎖 <b>Награда:</b> { $status_emoji }

user_statuses_message = 💠 Выберите статус, который будет отображаться в комментариях

status_not_found_message = ‼️ Статус не найден

achievement_property_not_found_message = ‼️ Код для получения достижения не найден

user_have_achievement_message = ‼️ У пользователя уже есть такое достижения

user_activated_achievement_message = ‼️ Вы уже получили достижение по этой ссылке

achievement_activation_from_date_message = ‼️ Время для получения достижения ещё не наступило

achievement_activation_until_date_message = ‼️ Время для получения достижения прошло

achievement_activated_success_message = 
    🏵 Вы получили достижение <b>«{ $achievement_name }»</b>
    
    💠 <b>Открыт новый статус:</b> { $status_emoji }

# Текста кнопок
nickname_button_text =
    { $is_changing ->
    [1] 📋 Сменить никнейм
    *[0] 📋 Выбрать никнейм
    }

achievements_button_text = 🏵 Достижения

statuses_button_text = 💠 Статусы

timetable_button_text = 📚 Расписание

profile_button_text = 📝 Профиль

back_to_main_button_text = ◀️ В главное меню

cancel_commenting_button_text = ❌ Отменить комментирование

confirm_timetable_add_button_text = ✅ Подтвердить

cancel_timetable_add_button_text = ❌ Отменить

back_button_text = ◀️ Назад

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

change_locale_button_text = 🌎 Изменить язык

delete_comment_button_text = ❌ Удалить комментарий

ban_comment_user_button_text = 🚫 Заблокировать

# Описания команд
start_command_description = 👑 Начать

timetable_command_description = 🗓 Добавить расписание