<template>
  <div id="app">
    <v-app id="inspire">
      <navbar />
      <v-row class="mb-6 mt-3">
        <v-col>
          <v-card class="mb-3">
            <breadcrumb
              :breadcrumb-names="breadcrumbNames"
              :breadcrumb-paths="breadcrumbPaths"
            />
          </v-card>

          <gym-info-card
            :gym-logo="gymLogo"
            :gym-name="gymName"
            :gym-website="gymWebsite"
            :gym-phone-number="gymPhoneNumber"
            :gym-rating="gymRating"
          />

          <photo-carousel :gym-photos="gymPhotos" />

          <map-card :map-active="mapActive" :gym-address="gymAddress" />

          <gym-hours-card
            :gym-times="gymTimes"
            :gym-name="gymName"
            :current-day-of-the-week="currentDayOfTheWeek"
          />

          <gym-reviews-card :gym-reviews="gymReviews" :gym-name="gymName" />

          <gym-leaderboard-card :gym-name="gymName" />
        </v-col>
        <v-col id="photo_column">
          <photo-column-card :gym-photos="gymPhotos" />
        </v-col>
      </v-row>
    </v-app>
  </div>
</template>

<script>
import Navbar from "~/components/Navbar.vue"
import Breadcrumb from "~/components/Breadcrumb.vue"
import GymInfoCard from "~/components/GymInfoCard.vue"
import PhotoCarousel from "~/components/PhotoCarousel.vue"
import MapCard from "~/components/MapCard.vue"
import GymHoursCard from "~/components/GymHoursCard.vue"
import GymReviewsCard from "~/components/GymReviewsCard.vue"
import GymLeaderboardCard from "~/components/GymLeaderboardCard.vue"
import PhotoColumnCard from "~/components/PhotoColumnCard.vue"

export default {
  components: {
    Navbar,
    Breadcrumb,
    GymInfoCard,
    PhotoCarousel,
    MapCard,
    GymHoursCard,
    GymReviewsCard,
    GymLeaderboardCard,
    PhotoColumnCard,
  },
  data() {
    return {
      gymRating: undefined,
      gymLogo: undefined,
      gymPhoneNumber: undefined,
      gymName: undefined,
      gymWebsite: undefined,
      gymAddress: undefined,
      gymLat: undefined,
      gymLon: undefined,
      gymReviews: undefined,
      gymPhotos: undefined,
      gymTimes: undefined,
      currentDayOfTheWeek: this.getCurrentDayOfTheWeek(),
      place_id: undefined,
      map: undefined,
      mapActive: false,
      service: undefined,
      breadcrumbNames: [],
      breadcrumbPaths: [],
    }
  },
  mounted() {
    this.maybeLoadGym()
  },
  methods: {
    maybeLoadGym() {
      if (this.$store.state.current_affiliate.name === undefined) {
        this.$retrievePathVariables(this.$store, this.$route.params)
        let that = this
        this.refreshStoredGym()
          .then((response) => {
            that.$store.commit("SET_CURRENT_AFFILIATE", response.results[0])
            this.initGymPage()
            return
          })
          .catch(function (error) {
            console.log(error)
          })
      }
      this.initGymPage()
    },
    refreshStoredGym() {
      const country = this.$store.state["current_country"]
      const state = this.$store.state["current_state"]
      const city = this.$store.state[`current_city`]
      const gymName = this.$store.state[`current_gym`]
      let url = `${process.env.BACKEND_URL}/affiliates/?name__iexact=${gymName}&city__iexact=${city}&country__iexact=${country}`
      if (state != this.$store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`

      url = encodeURI(url)
      return this.$axios.$get(url)
    },
    initGymPage() {
      this.setGymAttributes()
      this.initMap()
    },
    setGymAttributes() {
      this.gymLogo = this.$store.state.current_affiliate.photo
      this.gymName = this.$store.state.current_affiliate.name
      this.gymWebsite = this.$store.state.current_affiliate.website
      this.gymLat = this.$store.state.current_affiliate.lat
      this.gymLon = this.$store.state.current_affiliate.lon
      this.gymAddress = this.getAddress()
      this.breadcrumbNames = [
        "Gyms",
        this.$store.state.current_affiliate.city,
        this.$store.state.current_affiliate.name,
      ]
      this.breadcrumbPaths = ["/", "", ""]
    },
    getCurrentDayOfTheWeek() {
      let currentDay = new Date().getDay()
      if (currentDay == 0) {
        this.currentDayOfTheWeek = 6
      } else {
        this.currentDayOfTheWeek = currentDay - 1
      }
      return this.currentDayOfTheWeek
    },
    initMap() {
      // eslint-disable-next-line no-undef
      var location = new google.maps.LatLng(this.gymLat, this.gymLon)
      var coordinates = {
        lat: parseFloat(this.gymLat),
        lng: parseFloat(this.gymLon),
      }

      // eslint-disable-next-line no-undef
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: location,
        zoom: 15,
      })

      var request = {
        query: this.gymName + " " + this.gymAddress,
        fields: ["name", "place_id", "geometry"],
      }

      // eslint-disable-next-line no-undef
      this.service = new google.maps.places.PlacesService(this.map)
      let that = this
      // eslint-disable-next-line no-unused-vars
      this.service.findPlaceFromQuery(request, function (results, status) {
        that.createMarker(coordinates, that.map)
        that.map.setCenter(coordinates)

        if (results != null) {
          that.place_id = results[0].place_id
          that.getPlaceDetails()
        } else {
          that.gymPhoneNumber = ""
          that.gymRating = -1
          that.gymReviews = []
          that.gymPhotos = []
          that.gymTimes = []
          that.gymTimes = []
          return
        }
      })
    },
    getPlaceDetails() {
      var request = {
        placeId: this.place_id,
        fields: [
          "formatted_phone_number",
          "rating",
          "review",
          "photos",
          "opening_hours",
        ],
      }

      // eslint-disable-next-line no-undef
      this.service = new google.maps.places.PlacesService(this.map)
      let that = this
      this.service.getDetails(request, function (place, status) {
        // eslint-disable-next-line no-undef
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          that.gymPhoneNumber = place.formatted_phone_number
          that.gymRating = place.rating || -1
          that.gymReviews = place.reviews || []
          that.gymPhotos = place.photos || []
          that.gymTimes = place.opening_hours || []
          that.gymTimes = that.gymTimes.weekday_text || []
        }
      })
    },
    createMarker(coordinates, map) {
      // eslint-disable-next-line no-undef
      new google.maps.Marker({
        map: map,
        position: coordinates,
      })
      this.mapActive = true
    },
    getAddress() {
      let gymFullAddress = this.$store.state.current_affiliate.address
      gymFullAddress += ", " + this.$store.state.current_affiliate.city
      gymFullAddress += ", " + this.$store.state.current_affiliate.full_state
      gymFullAddress += " " + this.$store.state.current_affiliate.zip
      return gymFullAddress
    },
  },
}
</script>

<style lang="scss" scoped>
#photo_column {
  @media (max-width: 960px) {
    display: none;
  }
}
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-track {
  background: transparent;
  border: 1px solid darkgray;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
  border-radius: 5px;
}
</style>
