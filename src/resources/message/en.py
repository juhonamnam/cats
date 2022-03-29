en = {
    'com.accept': 'Accept',
    'com.reject': 'Reject',
    'com.noauth': 'You have no permission.',
    'com.success': 'Success',
    'com.failed': 'Failed',
    'com.yes': 'Yes',
    'com.no': 'No',
    'com.exit': 'Exit',
    # HTML
    'start.default': 'Hello {name}!! This is a test version of cryptocurrency trade algorithm project.\n\nWe provide cryptocurrency trading strategy in real time. Subscribe to our service to take advantage of what we provide.',
    'start.request': 'Subscribe',
    'start.request.sent': 'Permission request has been sent to the admin. If the admin accept your request, you will be registered to our service.',
    'start.alr_subscribed': 'You are already subscribed to our service.',
    'start.alr_subscribedmess': '{} is alreay subscribed.',
    'start.request.acceptmess': '{} is successfully subscribed.',
    'start.request.accept': 'You are successfully subscribed to our service!!\n\nFor more information about our service, use /about command. You can change your setting using /setting command',
    'start.request.rejectmess': '{}\'s request is rejected.',
    'start.requestmess': '{} requested to be subscribed.',
    # HTML
    'setting.default': '<b><u>CURRENT INFO</u></b>\n\n<b>Name:</b> {name}\n<b>Activity State:</b> {activity_state}',
    'setting.activitystate': 'Activity State',
    'setting.unsubscribe': 'Unsubscribe',
    'setting.activate': 'Activate',
    'setting.deactivate': 'Deactivate',
    'setting.active': 'Active',
    'setting.inactive': 'Inactive',
    # HTML
    'setting.backtosetting': 'Back to setting',
    # HTML
    'setting.activate.confirm': '<b>Current Activity State: Inactive</b>\n\nWill you activate?',
    # HTML
    'setting.deactivate.confirm': '<b>Current Activity State: Active</b>\n\nIf you deactivate, you will no longer receive real time buy & sell signals. Will you deactivate?',
    'setting.editname': 'Edit Name',
    # HTML
    'setting.editnameinput': '<i>Enter new name</i>',
    'setting.editnameinput.placeholder': 'Enter new name',
    # HTML
    'setting.editname.confirm': 'Your name will changed to <i>"{new_name}"</i>. Is it correct?',
    'setting.unsubscribe.confirm': 'Are you sure you want to unsubscribe?',
    # HTML
    'setting.language.curr': '<b>Current Language: English</b>',
    # HTML
    'usermanage.page': '<b><u>USER MANAGEMENT</u></b>\n\n<b>Total:</b> {}\n<b>Current Page:</b> {}',
    'usermanage.notsub': 'This user is no longer subscribed',
    'usermanage.noaccessadm': 'You have no access to other admin',
    'usermanage.alr_admin': 'This user is already an admin',
    'usermanage.prom': 'Promote to admin',
    'usermanage.susp': 'Suspend this user',
    # HTML
    'usermanage.default': '<b><u>USER INFO</u></b>\n\n<b>Chat ID:</b> {chat_id}\n<b>Name:</b> {name}\n<b>Language:</b> {language}\n<b>Activity State:</b> {activity_state}',
    'usermanage.prom.confirm': 'Are you sure you want to promote {} to admin?',
    'usermanage.backtolist': 'Back to user list',
    'usermanage.prom.success': 'The admin promoted you to an admin. You can now use /user_manage command to manage other users',
    'usermanage.susp.option1': 'Suspend',
    'usermanage.susp.option2': 'Suspend and Block',
    'usermanage.susp.confirm': 'Are you sure you want to suspend {}?',
    'buysig': '\n'.join([
                '--Buy {ticker}--',
                'Current Price: {curr_price}'
    ]),
    'sellsig': '\n'.join([
        '--Sell {ticker}--',
        'Sell Price: {sell_price}',
        'buy Price: {buy_price}',
        'Interest: {interest}%'
    ]),
}
