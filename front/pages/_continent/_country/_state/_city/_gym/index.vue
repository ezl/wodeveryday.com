<template>
  <div id="app">
    <v-app id="inspire">
      <navbar />
      <breadcrumb
        :breadcrumb-names="$store.state.globalBreadcrumbNames"
        :breadcrumb-paths="$store.state.globalBreadcrumbPaths"
      />
      <gym-navbar
        :navbar-active="navbarActive"
        :goto-elements="$store.state.gymNavbarGotoElements"
        :navbar-options="$store.state.gymNavbarOptions"
      />
      <v-row>
        <v-col v-if="windowInnerWidth > 540">
          <info-card
            class="mb-3"
            :gym-logo="gymLogo"
            :gym-name="gymName"
            :gym-website="gymWebsite"
            :gym-phone-number="gymPhoneNumber"
            :gym-rating="gymRating"
          />
          <reviews-card
            id="reviews"
            class="mb-3"
            :gym-reviews="gymReviews"
            :gym-name="gymName"
          />
        </v-col>
        <v-col id="keyInfo">
          <info-card
            v-if="windowInnerWidth <= 540"
            class="mb-3"
            :gym-logo="gymLogo"
            :gym-name="gymName"
            :gym-website="gymWebsite"
            :gym-phone-number="gymPhoneNumber"
            :gym-rating="gymRating"
          />
          <contact-info-card
            class="mb-3"
            :gym-website="gymWebsite"
            :gym-phone-number="gymPhoneNumber"
          />
          <hours-card
            class="mb-3"
            :gym-times="gymTimes"
            :gym-name="gymName"
            :current-day-of-the-week="currentDayOfTheWeek"
          />
          <price-card class="mb-3" :gym-website="gymWebsite" />
          <address-card class="mb-3" :gym-address="gymAddress" />
          <reviews-card
            v-if="windowInnerWidth <= 540"
            id="reviews"
            class="mb-3"
            :gym-reviews="gymReviews"
            :gym-name="gymName"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <span id="photos">
            <photo-grid id="photoGrid" :gym-photos="gymPhotos" />
            <photo-carousel :gym-photos="gymPhotos" />
          </span>
          <leaderboard-card id="leaderboard" :gym-name="gymName" />
          <map-card :map-active="mapActive" :gym-address="gymAddress" />
        </v-col>
      </v-row>
    </v-app>
  </div>
</template>

<script>
import Navbar from "~/components/Navbar.vue"
import Breadcrumb from "~/components/Breadcrumb.vue"
import InfoCard from "~/components/InfoCard.vue"
import PhotoCarousel from "~/components/PhotoCarousel.vue"
import MapCard from "~/components/MapCard.vue"
import HoursCard from "~/components/HoursCard.vue"
import ReviewsCard from "~/components/ReviewsCard.vue"
import LeaderboardCard from "~/components/LeaderboardCard.vue"
import PhotoGrid from "~/components/PhotoGrid.vue"
import ContactInfoCard from "~/components/ContactInfoCard.vue"
import AddressCard from "~/components/AddressCard.vue"
import GymNavbar from "~/components/GymNavbar.vue"
import PriceCard from "~/components/PriceCard.vue"

export default {
  components: {
    Navbar,
    Breadcrumb,
    InfoCard,
    ContactInfoCard,
    AddressCard,
    PhotoGrid,
    PhotoCarousel,
    MapCard,
    HoursCard,
    ReviewsCard,
    LeaderboardCard,
    GymNavbar,
    PriceCard,
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
      navbarOptions: ["Key Info"],
      gotoElements: ["#keyInfo"],
      navbarActive: false,
      windowInnerWidth: 0,
    }
  },
  computed: {
    fetchGymSearchQuery: function () {
      const query =
        this.$store.state.current_affiliate.name +
        " " +
        this.$store.state.current_affiliate.city +
        " " +
        this.$store.state.current_affiliate.country
      return query
    },
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.$generateBreadcrumb(this.$store, this.$route.params, "gym")

    // empty navbar for refill
    this.$store.commit("SET_GYM_NAVBAR_OPTIONS", [])
    this.$store.commit("SET_GYM_NAVBAR_GOTO_ELEMENTS", [])

    this.maybeLoadGym()
  },
  created() {
    if (process.client) window.addEventListener("resize", this.handleResize)
    this.handleResize()
  },
  destroyed() {
    if (process.client) window.removeEventListener("resize", this.handleResize)
  },
  methods: {
    handleResize() {
      if (process.client) this.windowInnerWidth = window.innerWidth
    },
    fillGymNavbar() {
      let navbarOptions = ["Key Info"]
      let gotoElements = ["#keyInfo"]

      if (this.gymReviews && this.gymReviews.length > 0) {
        navbarOptions.push("Reviews")
        gotoElements.push("#reviews")
      }

      navbarOptions.push("Map")
      gotoElements.push("#map")

      if (this.gymReviews && this.gymPhotos.length > 0) {
        navbarOptions.push("Photos")
        gotoElements.push("#photos")
      }

      this.$store.commit("UNSHIFT_TO_GYM_NAVBAR_OPTIONS", navbarOptions)
      this.$store.commit("UNSHIFT_TO_GYM_NAVBAR_GOTO_ELEMENTS", gotoElements)

      this.navbarActive = true
    },
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
      } else {
        this.initGymPage()
      }
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
        query: this.fetchGymSearchQuery,
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
          that.fillGymNavbar()
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
          that.gymPhoneNumber = place.formatted_phone_number || ""
          that.gymRating = place.rating || -1
          that.gymReviews = place.reviews || []
          that.gymPhotos = place.photos || []
          that.gymPhotos = that.gymPhotos.slice(0, 9)
          that.gymTimes = place.opening_hours || []
          that.gymTimes = that.gymTimes.weekday_text || []
          that.fillGymNavbar()
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
      if (this.$store.state.current_affiliate.full_state)
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
#photoGrid {
  @media (max-width: 960px) {
    display: none;
  }
}
.col {
  padding-top: 0px;
  padding-bottom: 0px;
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
