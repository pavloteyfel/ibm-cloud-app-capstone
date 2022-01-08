const main = (message) => {
    const connection = getCloudantConnection(message.API_URL, message.API_KEY);

    let reviewDb = connection.use("reviews");

    if (message.dealerId) {
        return new Promise((resolve, reject) => {
            reviewDb.find({ selector: { dealership: parseInt(message.dealerId) } },
                (error, result) => {
                    if (error) { reject(error) };
                    resolve(filter(result.docs[0]));
                }
            );
        });
    }

    return new Promise((resolve, reject) => {
        reviewDb.list({ include_docs: true }, (error, result) => {
            if (error) { reject(error) }
            if (result.rows.length == 0) {
                resolve({
                    dealerships: {},
                    total: 0,
                });
            }

            resolve({
                reviews: result.rows.map((row) => {
                    return filter(row.doc);
                }),
                total: result.rows.length,
            });
        });
    });
};

const getCloudantConnection = (url, key) => {
    const Cloudant = require("@cloudant/cloudant");
    const connection = Cloudant({
        url: url,
        plugins: { iamauth: { iamApiKey: key } },
    });
    return connection;
};

const filter = (entity) => {
    delete entity._id;
    delete entity._rev;
    return entity;
};
