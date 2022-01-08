const main = (message) => {

    if (!message.review) {
        return Promise.reject({ error: 'no review was sent' });
    }

    if (!message.review.name || !message.review.review) {
        return Promise.reject({ error: 'no name or review' });
    }

    const connection = getCloudantConnection(message.API_URL, message.API_KEY);

    const db = connection.use("reviews");

    return insert(db, message.review);

}

const getCloudantConnection = (url, key) => {
    const Cloudant = require("@cloudant/cloudant");
    const connection = Cloudant({
        url: url,
        plugins: { iamauth: { iamApiKey: key } },
    });
    return connection;
};

const insert = (db, doc) => {
    return new Promise((resolve, reject) => {
        db.insert(doc, (error, response) => {
            if (!error) {
                resolve(response);
            } else {
                console.log('error', error);
                reject(error);
            }
        });
    });
}

