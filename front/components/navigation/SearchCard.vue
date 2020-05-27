<template>
  <v-content>
    <navbar />
    <breadcrumb
      :breadcrumb-names="$store.state.globalBreadcrumbNames"
      :breadcrumb-paths="$store.state.globalBreadcrumbPaths"
    />
    <v-row align="center" justify="center" style="flex-direction: column;">
      <h1 class="ma-4">
        Find a Gym Anywhere
      </h1>
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-4 elevation-12">
          <v-autocomplete
            v-model="selectedItem"
            :items="flat(Object.values(itemList))"
            :loading="isLoading()"
            color="white"
            hide-no-data
            hide-selected
            placeholder="Start typing to Search"
            return-object
            @change="selectSubitem(selectedItem)"
          />
        </v-card>
      </v-col>
      <h1 v-if="itemTitle" class="mt-4 text-capitalize">
        {{ $store.state["current_" + itemTitle] }}
      </h1>
    </v-row>
    <v-row justify="center" class="flex-nowrap">
      <v-col
        v-for="(subList, index) in listOfItemLists"
        :key="index"
        :style="`width: ${columnWidth}%;`"
      >
        <v-list v-for="(subItems, item) in subList" :key="item" class="ma-4">
          <v-list-item-group color="primary">
            <v-list-item @click="selectItem(item)">
              <v-list-item-content>
                <v-list-item-title
                  class="headline font-weight-bold"
                  v-text="item"
                />
              </v-list-item-content>
            </v-list-item>
            <v-list-item
              v-for="(subItem, i) in subItems"
              :key="i"
              @click="selectSubitem(subItem)"
            >
              <v-list-item-content>
                <v-list-item-title v-text="subItem" />
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
  </v-content>
</template>

<script>
import Navbar from "~/components/global/Navbar.vue"
import Breadcrumb from "~/components/global/Breadcrumb.vue"
import _ from "lodash"

export default {
  name: "SearchCard",
  components: {
    Navbar,
    Breadcrumb,
  },
  props: {
    itemTitle: {
      type: String,
      required: false,
      default: undefined,
    },
    itemList: {
      type: Object,
      required: false,
      default: undefined,
    },
    selectItem: {
      type: Function,
      default: () => {},
    },
    selectSubitem: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      selectedItem: undefined,
      windowInnerWidth: 0,
      listOfItemLists: [],
      columnWidth: 0,
      breadcrumbNames: undefined,
    }
  },
  watch: {
    itemList: function () {
      this.listOfItemLists = this.divideObjectIntoListOfObjects(this.itemList)
    },
  },
  mounted() {
    this.handleResize()
  },
  created() {
    if (process.client) window.addEventListener("resize", this.handleResize)
    this.handleResize()
  },
  destroyed() {
    if (process.client) window.removeEventListener("resize", this.handleResize)
  },
  methods: {
    isLoading() {
      return (
        this.itemList === undefined || Object.values(this.itemList).length === 0
      )
    },
    handleResize() {
      if (process.client) this.windowInnerWidth = window.innerWidth
      this.listOfItemLists = this.divideObjectIntoListOfObjects(this.itemList)
      this.columnWidth = Math.floor(100 / (this.windowInnerWidth / 250))
    },
    divideObjectIntoListOfObjects(obj) {
      let divideInto = Math.floor(this.windowInnerWidth / 250)
      let objectKeys = Object.keys(obj)
      const objectSize = objectKeys.length

      let listOfObjectsSize = Math.floor(objectSize / divideInto)
      while (listOfObjectsSize === 0) {
        divideInto -= 1
        listOfObjectsSize = Math.floor(objectSize / divideInto)
      }

      let listOfObjects = []
      for (let i = 0; i < divideInto; i++) {
        if (i + 1 === divideInto) {
          let subset = _.pick(obj, objectKeys)
          listOfObjects.unshift(subset)
        } else {
          let subset = _.pick(obj, objectKeys.slice(0, listOfObjectsSize))
          listOfObjects.unshift(subset)
          objectKeys = objectKeys.slice(listOfObjectsSize)
        }
      }
      return listOfObjects
    },
    flat(input, depth = 1, stack) {
      const validStack = stack || []
      for (let item of input) {
        if (item instanceof Array && depth > 0) {
          this.flat(item, depth - 1, validStack)
        } else {
          validStack.push(item)
        }
      }

      return validStack
    },
  },
}
</script>
