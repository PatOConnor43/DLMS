const APP_URLS = {
    CONTENTS_LIST: '/api/contents/',
    DIRLAYOUT_LIST: '/api/dirlayouts/',
    DIRLAYOUT_DETAIL: '/api/dirlayouts/${id}/',
    DIRLAYOUT_CLONE: '/api/dirlayouts/${id}/clone/',
    DIRECTORY_LIST: '/api/directories/',
    DIRECTORY_DETAIL: '/api/directories/${id}/',
    TAG_LIST: '/api/tags/'
}

function get_url(templateStringLiteral, context) {
    context = context || {};
    Object.keys(context).forEach(eachKey => {
        templateStringLiteral = templateStringLiteral.replace("${" + eachKey +"}", context[eachKey]);
    })
    return templateStringLiteral;
}

module.exports = {
    APP_URLS: APP_URLS,
    get_url: get_url
}
