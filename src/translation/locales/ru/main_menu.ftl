#################### ГЛАВНОЕ МЕНЮ ####################

welcome_message =
    🚀 <b>Начни получать анонимные сообщения прямо сейчас!</b>

    🔖<b>Твоя ссылка (нажмите на неё, чтобы скопировать):</b>
    <code>{ $link }</code>


invalid_start_link_message = ❌ Вы перешли по непраавильной ссылке

user_is_blocked_message = 😔 Пользователь, котормоу вы хотите отправить сообщение, заблокировал нашего бота

send_anonim_message_message =
    ℹ️ Отправьте ваше сообщение, а мы перешлем его пользователю

new_anonim_message_message =
    🚀 <b>У вас новое анонимное сообщение!</b>

    👤 <b>Пользователь:</b> #{ $user_hash }

    { $anonim_message }

    ℹ️ Нажите кнопку, чтобы ответить

anonim_message_sent_message = ✅ Ваше сообщение успешно отправлено

user_info_message =
    <b>ID:</b> #{ $user_id } (<a href="tg://user?id={ $user_id }">Ссылка</a>)
    <b>Имя:</b> { $name }
    <b>Ник:</b> { $has_username ->
        [1] @{ $username }
        *[0] Не указан
    }


#################### ГЛАВНОЕ МЕНЮ ####################
