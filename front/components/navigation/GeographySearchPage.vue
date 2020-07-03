<template>
  <v-content>
    <navbar />
    <breadcrumb />
    <v-row align="center" justify="center" style="flex-direction: column;">
      <h1 class="ma-4">
        Find a Gym Anywhere
      </h1>
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-4 elevation-12">
          <v-autocomplete
            v-model="selectedItem"
            :items="getSearchableList"
            :loading="isLoading()"
            color="white"
            hide-no-data
            hide-selected
            placeholder="Start typing to Search"
            return-object
            @change="selectSubitemPrefetch(null, selectedItem)"
          />
        </v-card>
      </v-col>
      <h1 v-if="itemTitle" class="mt-4 text-capitalize">
        {{ getSearchPageTitle }}
      </h1>
    </v-row>
    <v-row v-if="listOfItemLists" justify="center" class="flex-nowrap">
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
              @click="selectSubitemPrefetch(item, subItem)"
            >
              <v-list-item-content>
                <v-list-item-title
                  v-if="typeof subItem === 'string'"
                  v-text="subItem"
                />
                <v-list-item-title
                  v-if="subItem && typeof subItem !== 'string'"
                  v-text="subItem[0]"
                />
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
  name: "GeographySearchPage",
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
      default: Object,
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
  computed: {
    getSearchPageTitle: function () {
      return this.$route.params[this.itemTitle].replace(/-/gi, " ")
    },
    getSearchableList: function () {
      if (!this.itemList) return []
      let searchableList = this.flat(Object.values(this.itemList))
      return searchableList
    },
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
    // TODO: remove this tech debt
    findParentAndSubItem(registryObject, name) {
      registryObject = Object.entries(registryObject)
      let parentAndSubItem = undefined
      for (let registryList of registryObject) {
        parentAndSubItem = registryList[1].find(
          (parent) => parent[0].indexOf(name) !== -1
        )
        if (parentAndSubItem !== undefined) {
          parentAndSubItem = [registryList[0], parentAndSubItem[1]]
          break
        }
      }

      return parentAndSubItem
    },
    findParent(registryObject, name) {
      registryObject = Object.entries(registryObject)
      const parentName = registryObject.find(
        (parent) => parent[1].indexOf(name) !== -1
      )
      return parentName[0]
    },
    selectSubitemPrefetch(item = null, subItem) {
      if (typeof subItem !== "string") subItem = subItem[1]
      if (
        !item &&
        Object.entries(this.itemList)[0] &&
        typeof Object.entries(this.itemList)[0][1][0] !== "string"
      ) {
        // TODO: remove this tech debt
        let itemAndSubItem = this.findParentAndSubItem(this.itemList, subItem)
        item = itemAndSubItem[0]
        subItem = itemAndSubItem[1]
      } else if (!item) {
        item = this.findParent(this.itemList, subItem)
      }
      this.selectSubitem(item, subItem)
    },
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
      let subset
      for (let i = 0; i < divideInto; i++) {
        if (i + 1 === divideInto) {
          subset = _.pick(obj, objectKeys)
          listOfObjects.unshift(subset)
        } else {
          subset = _.pick(obj, objectKeys.slice(0, listOfObjectsSize))
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
