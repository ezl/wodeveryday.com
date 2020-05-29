<template>
  <div>
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
      <v-col v-show="windowInnerWidth > 540">
        <info-card
          class="mb-3"
          :gym-phone-number="gymPhoneNumber"
          :gym-rating="gymRating"
        />
        <reviews-card
          :id="windowInnerWidth > 540 ? 'reviews' : ''"
          class="mb-3"
          :gym-reviews="gymReviews"
        />
      </v-col>
      <v-col id="keyInfo">
        <info-card
          v-show="windowInnerWidth <= 540"
          class="mb-3"
          :gym-phone-number="gymPhoneNumber"
          :gym-rating="gymRating"
        />
        <contact-info-card class="mb-3" :gym-phone-number="gymPhoneNumber" />
        <hours-card
          class="mb-3"
          :gym-times="gymTimes"
          :current-day-of-the-week="currentDayOfTheWeek"
        />
        <price-card class="mb-3" />
        <address-card class="mb-3" :gym-address="gymAddress" />
        <reviews-card
          v-show="windowInnerWidth <= 540"
          :id="windowInnerWidth <= 540 ? 'reviews' : ''"
          class="mb-3"
          :gym-reviews="gymReviews"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <span id="photos">
          <photo-grid id="photoGrid" :gym-photos="gymPhotos" />
          <photo-carousel :gym-photos="gymPhotos" />
        </span>
        <leaderboard-card id="leaderboard" />
        <map-card :map-active="mapActive" :gym-address="gymAddress" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Navbar from "~/components/global/Navbar.vue"
import Breadcrumb from "~/components/global/Breadcrumb.vue"
import InfoCard from "~/components/gym_page/InfoCard.vue"
import PhotoCarousel from "~/components/gym_page/PhotoCarousel.vue"
import MapCard from "~/components/gym_page/MapCard.vue"
import HoursCard from "~/components/gym_page/HoursCard.vue"
import ReviewsCard from "~/components/gym_page/ReviewsCard.vue"
import LeaderboardCard from "~/components/gym_page/LeaderboardCard.vue"
import PhotoGrid from "~/components/gym_page/PhotoGrid.vue"
import ContactInfoCard from "~/components/gym_page/ContactInfoCard.vue"
import AddressCard from "~/components/gym_page/AddressCard.vue"
import GymNavbar from "~/components/gym_page/GymNavbar.vue"
import PriceCard from "~/components/gym_page/PriceCard.vue"
import actions from "~/store/actions.js"

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
      gymPhoneNumber: undefined,
      gymAddress: undefined,
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
        this.$store.state.gym_object.name +
        " " +
        this.$store.state.gym_object.city +
        " " +
        this.$store.state.gym_object.country
      return query
    },
    fetchGymURL: function () {
      const country = this.$store.state["current_country"]
      const state = this.$store.state["current_state"]
      const city = this.$store.state[`current_city`]
      const gymName = this.$store.state[`current_gym`]
      let url = `${process.env.BACKEND_URL}/affiliates/?name__iexact=${gymName}&city__iexact=${city}&country__iexact=${country}`
      if (state != this.$store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`

      url = encodeURI(url)
      return url
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
      if (this.$store.state.gym_object.name === undefined) {
        this.$retrievePathVariables(this.$store, this.$route.params)
        const url = this.fetchGymURL
        actions.retrieveGym(url, this.$store).then(() => {
          this.initGymPage()
          return
        })
      } else {
        this.initGymPage()
      }
    },
    initGymPage() {
      this.gymAddress = this.getAddress()
      this.initMap()
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
      var location = new google.maps.LatLng(
        this.$store.state.gym_object.lat,
        this.$store.state.gym_object.lon
      )
      var coordinates = {
        lat: parseFloat(this.$store.state.gym_object.lat),
        lng: parseFloat(this.$store.state.gym_object.lon),
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
      let gymFullAddress = this.$store.state.gym_object.address
      gymFullAddress += ", " + this.$store.state.gym_object.city
      if (this.$store.state.gym_object.full_state)
        gymFullAddress += ", " + this.$store.state.gym_object.full_state
      gymFullAddress += " " + this.$store.state.gym_object.zip
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
