import axios from "axios"

/* eslint-disable no-unused-vars */
export default {
  async get(url, params) {
    try {
      const data = await axios.get(url, { params: params })
      return data
    } catch (error) {
      throw new Error(error)
    }
  },
}
