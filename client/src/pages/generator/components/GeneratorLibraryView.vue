<script setup lang="ts">

import {ref, watch, onBeforeMount} from "vue";
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
    return true
  if (_.map(dopBook.value, (x) => x.id).includes(id))
    return true
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
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-discipline-library/`, {
    library: {
      mainBook: mainBook.value,
      dopBook: dopBook.value,
    }
  })
  $q.loading.hide()
}

async function addBook() {
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
      saveLibary()
    })
}

watch(disciplineLibrary, () => {
  if (disciplineLibrary.value?.mainBook?.length)
    mainBook.value = disciplineLibrary.value?.mainBook
  if (disciplineLibrary.value?.dopBook?.length)
    dopBook.value = disciplineLibrary.value?.dopBook
})

onBeforeMount(() => {
  if (disciplineLibrary.value?.mainBook?.length)
    mainBook.value = disciplineLibrary.value?.mainBook
  if (disciplineLibrary.value?.dopBook?.length)
    dopBook.value = disciplineLibrary.value?.dopBook
})


</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Учебная литература для дисциплины</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn
        class="q-mb-md"
        label="Добавить книгу"
        color="secondary"
        @click="addBook"
      />
      <div class="row q-gutter-x-md q-mb-md">
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
                  <div class="q-gutter-x-md q-mt-md">
                    <q-btn color="red" label="Убрать"
                           @click="deleteMainBook(item.id)"/>
                  </div>
                </div>
              </template>
            </q-field>
          </div>
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
                  <div class="q-gutter-x-md q-mt-md">
                    <q-btn :disabled="checkTaken(item.id)" color="primary" label="В основную литературу"
                           @click="addMainBook(item)"/>
                    <q-btn :disabled="checkTaken(item.id)" color="secondary" label="В дополнительную литературу"
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
