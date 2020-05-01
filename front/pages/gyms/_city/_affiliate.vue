<template>
  <div id="app">
    <v-app id="inspire">
      <v-card>
        <v-tabs v-model="currentNavTab" dark show-arrows centered>
          <v-tabs-slider />

          <v-tab
            v-for="(tab, index) in navbarTabs"
            :key="index"
            :disabled="index == 3"
          >
            <h1 v-if="index == 3" style="color: white; opacity: 1;">
              {{ tab }}
            </h1>
            <span v-if="index != 3">{{ tab }}</span>
          </v-tab>
        </v-tabs>
      </v-card>

      <v-row class="mb-6 mt-3">
        <v-col>
          <drilldown :gym-name="gymName" />

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
import Drilldown from "~/components/Drilldown.vue"
import GymInfoCard from "~/components/GymInfoCard.vue"
import PhotoCarousel from "~/components/PhotoCarousel.vue"
import MapCard from "~/components/MapCard.vue"
import GymHoursCard from "~/components/GymHoursCard.vue"
import GymReviewsCard from "~/components/GymReviewsCard.vue"
import GymLeaderboardCard from "~/components/GymLeaderboardCard.vue"
import PhotoColumnCard from "~/components/PhotoColumnCard.vue"

export default {
  components: {
    Drilldown,
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
      currentNavTab: 1,
      navbarTabs: [
        "Home",
        "Find A Gym",
        "Games",
        "WOD EVERY DAY",
        "About",
        "Contact",
        "Blog",
      ],
      gymRating: undefined,
      gymLogo: this.$store.state.current_affiliate.photo,
      gymPhoneNumber: undefined,
      gymName: this.$store.state.current_affiliate.name,
      gymWebsite: this.$store.state.current_affiliate.website,
      gymAddress: this.getAddress(),
      gymLat: this.$store.state.current_affiliate.lat,
      gymLon: this.$store.state.current_affiliate.lon,
      gymReviews: undefined,
      gymPhotos: undefined,
      gymTimes: undefined,
      currentDayOfTheWeek: this.getCurrentDayOfTheWeek(),
      place_id: undefined,
      map: undefined,
      mapActive: false,
      service: undefined,
    }
  },
  mounted() {
    this.initMap()
  },
  methods: {
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
      var sydney = new google.maps.LatLng(this.gymLat, this.gymLon)

      // eslint-disable-next-line no-undef
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: sydney,
        zoom: 15,
      })

      var request = {
        query: this.gymName + " " + this.gymAddress,
        fields: ["name", "place_id", "geometry"],
      }

      // eslint-disable-next-line no-undef
      this.service = new google.maps.places.PlacesService(this.map)
      let that = this
      this.service.findPlaceFromQuery(request, function (results, status) {
        that.place_id = results[0].place_id
        // eslint-disable-next-line no-undef
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          for (var i = 0; i < results.length; i++) {
            that.createMarker(results[i], that.map)
          }
          that.map.setCenter(results[0].geometry.location)
        }
        that.getPlaceDetails()
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
    createMarker(place, map) {
      // eslint-disable-next-line no-undef
      new google.maps.Marker({
        map: map,
        position: place.geometry.location,
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
