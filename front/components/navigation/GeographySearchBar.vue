<template>
  <v-row
    align="center"
    justify="center"
    style="flex-direction: row; width: 80%;"
  >
    <v-col cols="8">
      <v-card class="pa-3">
        <v-autocomplete
          v-model="selectedGymItem"
          :items="gymItems"
          :loading="gymSearchIsLoading"
          :search-input.sync="gymSearch"
          item-text="name"
          color="white"
          placeholder="Search for a Gym"
          return-object
          no-filter
        />
      </v-card>
    </v-col>
    <v-col>
      <v-card class="pa-3">
        <v-autocomplete
          v-model="selectedLocationItem"
          :items="locationItems"
          :loading="locationSearchIsLoading"
          :search-input.sync="locationSearch"
          color="white"
          placeholder="Search for a location"
          return-object
          no-filter
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import apiLibrary from "~/store/apiLibrary.js"

export default {
  name: "GeographySearchBar",
  props: {
    itemList: {
      type: Object,
      required: false,
      default: Object,
    },
    selectSubitemPrefetch: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      locationSearchIsLoading: false,
      gymSearchIsLoading: false,
      locationItemsResponse: [],
      gymItemsResponse: [],
      locationSearch: null,
      gymSearch: null,
      selectedLocationItem: null,
      selectedGymItem: null,
    }
  },
  computed: {
    getSearchableList: function () {
      if (!this.itemList) return []
      let searchableList = this.flat(Object.values(this.itemList))
      return searchableList
    },
    isLoading: function () {
      return (
        this.itemList === undefined || Object.values(this.itemList).length === 0
      )
    },
    locationItems() {
      return this.locationItemsResponse
    },
    gymItems() {
      return this.gymItemsResponse
    },
  },
  watch: {
    gymSearch(searchText) {
      if (!searchText) return

      clearTimeout(this._timerId)
      this._timerId = setTimeout(() => {
        this.fetchGyms(searchText)
      }, 600)
    },
    locationSearch(searchText) {
      if (!searchText) return

      clearTimeout(this._timerId)
      this._timerId = setTimeout(() => {
        this.fetchLocations(searchText)
      }, 600)
    },
  },
  methods: {
    fetchGyms(searchText) {
      this.gymSearchIsLoading = true
      const url = `${process.env.BACKEND_URL}/gyms/?search=${searchText}`
      apiLibrary
        .retrieveGyms(url)
        .then((response) => {
          this.gymItemsResponse = response
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => (this.gymSearchIsLoading = false))
    },
    fetchLocations(searchText) {
      this.locationSearchIsLoading = true
      const url = `${process.env.BACKEND_URL}/gyms/search_locations/?search_text=${searchText}`
      apiLibrary
        .searchLocations(url)
        .then((response) => {
          this.locationItemsResponse = response
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => (this.locationSearchIsLoading = false))
    },
    flat(input, depth = 1, stack) {
      const validStack = stack || []
      for (let item of input) {
        if (item instanceof Array && depth > 0) {
          this.flat(item, depth - 1, validStack)
        } else {
          // TODO: remove this tech debt
          if (item && typeof item !== "string") item = item[0]
          validStack.push(item)
        }
      }

      return validStack
    },
  },
}
</script>
