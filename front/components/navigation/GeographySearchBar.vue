<template>
  <v-row
    align="center"
    justify="center"
    style="flex-direction: row; width: 80%;"
  >
    <v-card class="pa-3" style="width: 100%;">
      <v-autocomplete
        v-model="selectedGymItem"
        :items="gymItems"
        :loading="gymSearchIsLoading"
        :search-input.sync="gymSearch"
        item-text="location_name"
        color="white"
        hide-selected
        placeholder="Search for a Gym or Location"
        return-object
        no-filter
        @change="goToLocation()"
      >
        <template v-slot:item="data">
          <v-list-item-content v-text="data.item.location_name" />
          <v-list-item-content class="text-right d-block">
            <v-btn
              style="pointer-events: none;"
              color="primary"
              v-text="data.item.location_type"
            />
          </v-list-item-content>
        </template>
        <template v-slot:append-item>
          <div v-if="resultsPageCount > 0" class="text-center">
            <v-pagination
              v-model="resultsPage"
              :total-visible="5"
              :length="resultsPageCount"
              circle
            />
          </div>
        </template>
      </v-autocomplete>
    </v-card>
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
  },
  data() {
    return {
      gymSearchIsLoading: false,
      gymItemsResponse: [],
      gymSearch: null,
      selectedGymItem: null,
      resultsPage: 1,
      currentSearchText: null,
      resultsPageCount: 0,
    }
  },
  computed: {
    gymItems() {
      return this.gymItemsResponse
    },
  },
  watch: {
    gymSearch(searchText) {
      if (
        !searchText ||
        (searchText && searchText.length < 3) ||
        (this.selectedGymItem &&
          searchText === this.selectedGymItem.location_name)
      )
        return

      clearTimeout(this._timerId)
      this._timerId = setTimeout(() => {
        if (searchText !== this.currentSearchText) this.resultsPage = 1
        this.currentSearchText = searchText
        this.fetchGyms(searchText)
      }, 600)
    },
    // eslint-disable-next-line no-unused-vars
    resultsPage(newValue, oldValue) {
      this.fetchGyms(this.currentSearchText, newValue)
    },
  },
  methods: {
    goToLocation() {
      this.$router.replace({ path: `/${this.selectedGymItem.location_path}` })
    },
    fetchGyms(searchText, page = 1) {
      this.gymSearchIsLoading = true
      const url = `${process.env.BACKEND_URL}/gyms/search_locations/?search_text=${searchText}&page=${page}`
      apiLibrary
        .searchLocations(url)
        .then((response) => {
          this.resultsPageCount = response.meta.total_pages
          this.gymItemsResponse = response.data
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => (this.gymSearchIsLoading = false))
    },
  },
}
</script>
