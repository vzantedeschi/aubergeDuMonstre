/* Notification zone */
notification = {
    show: function(cls, msg) {
        msg = preprocessText(msg);
        $('#notification-bar').attr('class', cls).stop().html(msg).show().fadeIn(500).delay(2000).fadeOut(500);
    },
    error: function(msg) {
        this.show('error', msg);
    },
    warning: function(msg) {
        this.show('warning', msg);
    },
    info: function(msg) {
        this.show('info', msg);
    },
    success: function(msg) {
        this.show('success', msg);
    }
}