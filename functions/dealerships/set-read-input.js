const main = (message) => {
    const connection = getCloudantConnection(message.API_URL, message.API_KEY);

    let dealershipDb = connection.use("dealerships");

    if (message.state) {
        return new Promise((resolve, reject) => {
            dealershipDb.find(
                {
                    selector: { st: { $eq: message.state } },
                },
                (error, result) => {
                    if (error) {
                        reject(error);
                    }
                    resolve({
                        dealerships: result.docs.map((dealership) => {
                            return dealershipFilter(dealership);
                        }),
                        total: result.docs.length,
                    });
                }
            );
        });
    }

    if (message.id) {
        return new Promise((resolve, reject) => {
            dealershipDb.find(
                {
                    selector: { id: parseInt(message.id) },
                },
                (error, result) => {
                    if (error) {
                        reject(error);
                    }
                    resolve(dealershipFilter(result.docs[0]));
                }
            );
        });
    }

    return new Promise((resolve, reject) => {
        dealershipDb.list({ include_docs: true }, (error, result) => {
            if (error) {
                reject(error);
            }

            if (result.rows.length == 0) {
                resolve({
                    dealerships: [],
                    total: 0,
                });
            }

            resolve({
                dealerships: result.rows.map((row) => {
                    return dealershipFilter(row.doc);
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

const dealershipFilter = (dealership) => {
    delete dealership._id;
    delete dealership._rev;
    return dealership;
};
