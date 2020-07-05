import axios from "axios"

/* eslint-disable no-unused-vars */
export default {
  async get(url, params) {
    url = encodeURI(url)
    const data = axios
      .get(url, { params: params })
      .then((result) => {
        return result.data
      })
      .catch((error) => {
        if (error.response) console.log(error.response)
      })
    return data
  },
}
