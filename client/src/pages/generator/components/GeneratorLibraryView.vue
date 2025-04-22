<script setup lang="ts">

import {ref, watch, onBeforeMount, watchEffect} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {GeneratorBookData} from "src/types";
import _ from "lodash";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import GeneratorAddBookDialog from "pages/generator/components/dialogs/GeneratorAddBookDialog.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore()

const {
  activeRpdId,
  disciplineLibrary,
  rpdData,
  disabled,
} = storeToRefs(generatorViewStore)


const searchVal = ref('')
const bookData = ref([])

const dopBook = ref<GeneratorBookData[]>([])
const mainBook = ref<GeneratorBookData[]>([])

const columns = ref([
  {name: 'name', label: 'Название', field: 'name', align: 'center'},
])

function checkTaken(id) {
  if (_.map(mainBook.value, (x) => x.id).includes(id))
    return 'main'
  if (_.map(dopBook.value, (x) => x.id).includes(id))
    return 'dop'
  return false
}

function addMainBook(data) {
  mainBook.value.push(data)
  saveLibary()
}

function addDopBook(data) {
  dopBook.value.push(data)
  saveLibary()
}

function deleteMainBook(id) {
  let key = _.findKey(mainBook.value, (x) => x.id == id)
  mainBook.value.splice(key, 1)
  saveLibary()
}

function deleteDopBook(id) {
  let key = _.findKey(dopBook.value, (x) => x.id == id)
  dopBook.value.splice(key, 1)
  saveLibary()
}

async function searchBook() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск книг"})
    let r = await api.get('/api/generator/search-book/', {params: {val: searchVal.value}})
    bookData.value = r.data
    $q.loading.hide()
  }
}

async function saveLibary() {
  // $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "library",
    value: {
      "mainBook": mainBook.value,
      "dopBook": dopBook.value,
    }
  })
  _.set(disciplineLibrary.value, "[0].value['mainBook']", mainBook.value)
  _.set(disciplineLibrary.value, "[0].value['dopBook']", dopBook.value)
  generatorViewStore.checkErrors()
  // $q.loading.hide()
}

async function addBook() {
  if (!disciplineLibrary.value[0]) {
    _.set(disciplineLibrary.value, "[0].value['mainBook']", [])
    _.set(disciplineLibrary.value, "[0].value['dopBook']", [])
    saveLibary()
  }
  $q.notify({
    message: "Убедитесь, что выбранный источник доступен всем студентам и в достаточном количестве.",
    color: "secondary",
    type: "info",
    position: "center",
    progress: true,
    timeout: 3500,
  })

  $q.dialog({
    component: GeneratorAddBookDialog,
  }).onOk(() => {
    mainBook.value = disciplineLibrary.value[0]?.value['mainBook'] || []
    dopBook.value = disciplineLibrary.value[0]?.value['dopBook'] || []
    saveLibary()
  })
}

watchEffect(() => {
  mainBook.value = disciplineLibrary.value[0]?.value['mainBook'] || []
  dopBook.value = disciplineLibrary.value[0]?.value['dopBook'] || []
})


</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6">Учебная литература для дисциплины</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn
        class="q-mb-md"
        label="Добавить книгу"
        color="secondary"
        @click="addBook"
        v-show="!disabled"
      />
      <div class="row q-gutter-x-md q-mb-md" v-show="!disabled">
        <q-input
          label="Введите текст для поиска"
          stack-label
          v-model="searchVal"
          filled
          class="col"
          :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
        />
        <q-btn color="secondary" @click="searchBook" label="Поиск"/>
      </div>
      <div class="row">
        <div class="col-6">
          <div class="text-h6">Основная литература</div>
          <div v-for="item in mainBook" style="width: 95%">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <a v-if="item.http_link" :href="`${item.http_link}`" target="_blank">{{ item.bib_disc }}</a>
                  <span v-else>{{ item.bib_disc }}</span>
                  <div class="q-gutter-x-md q-mt-md" v-show="!disabled">
                    <q-btn color="red" label="Убрать"
                           @click="deleteMainBook(item.id)"/>
                  </div>
                </div>
              </template>
            </q-field>
          </div>
          <q-separator/>
          <div class="text-h6">Дополнительная литература</div>
          <div v-for="item in dopBook" style="width: 95%">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <a v-if="item.http_link" :href="`${item.http_link}`" target="_blank">{{ item.bib_disc }}</a>
                  <span v-else>{{ item.bib_disc }}</span>
                  <div class="q-gutter-x-md q-mt-md">
                    <q-btn color="red" label="Убрать"
                           @click="deleteDopBook(item.id)"/>
                  </div>
                </div>
              </template>
            </q-field>
          </div>
        </div>
        <div class="col-6">
          <div v-for="item in bookData">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <a v-if="item.http_link" :href="`${item.http_link}`" target="_blank">{{ item.bib_disc }}</a>
                  <span v-else>{{ item.bib_disc }}</span>
                  <div v-if="checkTaken(item.id)">
                    <q-btn v-if="checkTaken(item.id) == 'main'" readonly>В основной литературе</q-btn>
                    <q-btn v-if="checkTaken(item.id) == 'dop'" readonly>В дополнительной литературе</q-btn>
                  </div>
                  <div v-else class="q-gutter-x-md q-mt-md">
                    <q-btn color="primary" :label="item.cnt < 10 && item.bib_disc.indexOf('[Электронный ресурс]') == -1 ? 'Недостаточно экземпляров' : 'В основную литературу'" :disabled="item.cnt < 10 && item.bib_disc.indexOf('[Электронный ресурс]') == -1"
                           @click="addMainBook(item)"/>
                    <q-btn color="secondary" label="В дополнительную литературу"
                           @click="addDopBook(item)"/>
                  </div>
                </div>
              </template>
            </q-field>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
