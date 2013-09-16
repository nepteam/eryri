function whenAgo(time, currentTime) {
    var diffInSecond = currentTime - time,
        diffInMinute = Math.floor(diffInSecond / 60),
        diffInHour   = Math.floor(diffInSecond / 60 / 60),
        diffInDay    = Math.floor(diffInSecond / 60 / 60 / 24);
    currentTime = currentTime || parseInt(new Date().getTime() / 1000, 10);

    switch (true) {
    case diffInDay > 0:
        return diffInDay + 'd';
    case diffInHour > 0:
        return diffInHour + 'h';
    case diffInMinute > 0:
        return diffInMinute + 'm';
    default:
        return 'now';
    }
}
