<script setup lang="ts">

import {useRouter} from "vue-router";
import {computed, onBeforeMount, ref, watch} from "vue";
import {useQuasar} from "quasar";
import {api} from "boot/axios";
import _ from "lodash";
import draggable from "vuedraggable";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";


const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

const router = useRouter()
const $q = useQuasar()

const mainStore = useMainStore();

const {FORCE_SCRIPT_NAME} = storeToRefs(mainStore);

const step = ref(0)

// const columns = [
//   {
//     name: 'ckaf',
//     field: 'ckaf',
//     label: 'Кафедра',
//     align: 'center',
//   },
//   {
//     name: 'name',
//     field: 'name',
//     label: 'Наименование ООП',
//     align: 'center',
//   },
//   {
//     name: 'cfac',
//     field: 'cfac',
//     label: 'Институт',
//     align: 'center',
//   },
//   {
//     name: 'range',
//     field: 'range',
//     label: 'Срок освоения',
//     align: 'center',
//   },
//   {
//     name: 'cfob',
//     field: 'cfob',
//     label: 'Форма обучения',
//     align: 'center',
//   },
//   {
//     name: 'startyear',
//     field: 'startyear',
//     label: 'Год начала обучения',
//     align: 'center',
//   },
//   {
//     name: 'fgt',
//     field: 'fgt',
//     label: 'ФГТ',
//     align: 'center',
//   },
//   {
//     name: 'viceRector',
//     field: 'viceRector',
//     label: 'Проректор по учебной работе',
//     align: 'center',
//   },
//   {
//     name: 'director',
//     field: 'director',
//     label: 'Директор института',
//     align: 'center',
//   },
//   {
//     name: 'zavkaf',
//     field: 'zavkaf',
//     label: 'Заведующий кафедрой',
//     align: 'center',
//   },
//   {
//     name: 'rop',
//     field: 'rop',
//     label: 'Руководитель ООП',
//     align: 'center',
//   },
//   {
//     name: 'year',
//     field: 'year',
//     label: 'Год',
//     align: 'center',
//   },
// ]

const columnsNames = {
  'ckaf': {label: 'Кафедра', visible: true},
  'name': {label: 'Наименование ООП', visible: true},
  'cfac': {label: 'Институт', visible: true},
  'rng': {label: 'Срок освоения', visible: true},
  'cfob': {label: 'Форма обучения', visible: true},
  'startyear': {label: 'Год начала обучения', visible: true},
  'fgt': {label: 'ФГТ', visible: true},
  'viceRector': {label: 'Проректор по учебной работе', visible: true},
  'director': {label: 'Директор института', visible: true},
  'zavkaf': {label: 'Заведующий кафедрой', visible: true},
  'rop': {label: 'Руководитель ООП', visible: true},
  'year': {label: 'Год', visible: true},
  'id': {label: 'Идентификатор', visible: false},
  'mira_id': {label: 'Идентификатор в mira', visible: false},
}

const columns = [
  {
    name: 'label',
    field: 'label',
    label: 'Параметр',
    align: 'center',
  },
  {
    name: 'val',
    field: 'val',
    label: 'Значение',
    align: 'center',
  },
]

const rows = ref([])
const kurs = ref()
const mainInfo = ref()
const scientificWorks = ref([])
const scientificData = ref([])

const work = ref()
const addWorkDialog = ref(false)

const scientificResearchAutumn = ref()
const scientificResearchWinter = ref()

const scientificResearch = computed(() => {
  return _.filter(scientificData.value, (x) => x.parameters.part == 0)
})

const scientificResearchBySemester = computed(() => {
  return _.groupBy(scientificResearch.value, x => x.parameters.semester)
})

const scientificDissertData = ref()
const scientificPublishData = ref()

const showHelpFirstPage = ref(true)
const showHelpSecondPage = ref(true)
const showHelpThirdPage = ref(true)
const showHelpFourPage = ref(true)

async function fetchPlanData() {
  let r = await api.get(`/api/generator/${props.id}/get-asp-program-detail/`)
  mainInfo.value = _.get(r.data, 'plan')
  _.forEach(r.data.plan, (x, key) => {
    if (columnsNames[key].visible) {
      rows.value.push({
        "key": key,
        "val": x,
        "label": columnsNames[key].label,
      })
    }
  })

  scientificData.value = r.data.data
}

async function fetchHandbook() {
  let r = await api.get('/api/generator/get-scientific-work/')
  scientificWorks.value = r.data
  scientificWorks.value.push({id: 0, name: ''})
}

async function saveMainInfo(data, key) {
  mainInfo.value[key] = data
  let r = await api.post(`/api/generator/${mainInfo.value.id}/save-asp-program-data/`, mainInfo.value)

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

}

async function detectMoveAutumn(evt) {
  $q.loading.show({message: "Сохранение данных"})
  scientificResearchAutumn.value = _.map(scientificResearchAutumn.value, (x, index) => {
    return {
      ...x,
      plan_id: mainInfo.value.id,
      parameters: {...x.parameters, order: index},
    }
  })
  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, scientificResearchAutumn.value)

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

  $q.loading.hide()
}

async function detectMoveWinter(evt) {
  $q.loading.show({message: "Сохранение данных"})
  scientificResearchWinter.value = _.map(scientificResearchWinter.value, (x, index) => {
    return {
      ...x,
      plan_id: mainInfo.value.id,
      parameters: {...x.parameters, order: index},
    }
  })
  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, scientificResearchWinter.value)

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

  $q.loading.hide()
}

async function detectMoveDissert(evt) {
  $q.loading.show({message: "Сохранение данных"})

  scientificDissertData.value = _.map(scientificDissertData.value, (x, index) => {
    return {
      ...x,
      plan_id: mainInfo.value.id,
      parameters: {...x.parameters, order: index},
    }
  })

  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, scientificDissertData.value)

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

  $q.loading.hide()
}

async function detectMovePublish(evt) {
  $q.loading.show({message: "Сохранение данных"})

  scientificPublishData.value = _.map(scientificPublishData.value, (x, index) => {
    return {
      ...x,
      plan_id: mainInfo.value.id,
      parameters: {...x.parameters, order: index},
    }
  })

  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, scientificPublishData.value)

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

  $q.loading.hide()
}

const currentItem = ref([])

function openAddWorkDialog(semester, type) {
  currentItem.value = {
    'part': type,
    'semester': semester,
    'order': _.last(scientificResearchBySemester.value[semester]) ? _.last(scientificResearchBySemester.value[semester]).parameters.order + 1 : 0
  }
  addWorkDialog.value = true
}

async function addWorkInScience() {
  $q.loading.show({message: "Сохранение данных"})
  const data = [
    {
      'parameters': currentItem.value,
      'text': work.value,
      'plan_id': mainInfo.value.id
    }
  ]
  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, data)
  addWorkDialog.value = false
  work.value = ''
  scientificData.value.push(r.data[0])
  scientificResearchAutumn.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 1).orderBy(x => x.parameters.order).value()
  scientificResearchWinter.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 2).orderBy(x => x.parameters.order).value()

  $q.notify({
    message: 'Успешно сохранено!',
    position: 'top-right',
    color: 'positive',
  })

  $q.loading.hide()
}

async function deleteWorkScience(id) {
  let r = await api.delete(`/api/generator/${id}/del-scientific-work/`)

  const key = _.findKey(scientificData.value, x => x.id == id)
  scientificData.value.splice(key, 1)
  scientificResearchAutumn.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 1).orderBy(x => x.parameters.order).value()
  scientificResearchWinter.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 2).orderBy(x => x.parameters.order).value()

  $q.notify({
    message: 'Успешно удалено :(',
    position: 'top-right',
    color: 'info',
  })
}

async function addRowDissertData() {
  const data = [{
    text: '',
    plan_id: mainInfo.value.id,
    parameters: {
      part: 1,
      order: _.last(scientificDissertData.value) ? _.last(scientificDissertData.value).parameters.order + 1 : 0,
      semester: 0,
    }
  }]
  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, data)
  scientificData.value.push(r.data[0])
  scientificDissertData.value = _(scientificData.value).filter(x => x.parameters.part == 1).orderBy(x => x.parameters.order).value()
}

async function addRowPublishData() {
  const data = [{
    text: '',
    plan_id: mainInfo.value.id,
    parameters: {
      part: 2,
      order: _.last(scientificPublishData.value) ? _.last(scientificPublishData.value).parameters.order + 1 : 0,
      semester: 0,
    }
  }]
  let r = await api.post(`/api/generator/${props.id}/save-scientific-data/`, data)
  scientificData.value.push(r.data[0])
  scientificPublishData.value = _(scientificData.value).filter(x => x.parameters.part == 2).orderBy(x => x.parameters.order).value()
}

async function deleteDissertData(id) {
  let r = await api.delete(`/api/generator/${id}/del-scientific-work/`)

  const key = _.findKey(scientificData.value, x => x.id == id)
  scientificData.value.splice(key, 1)
  scientificDissertData.value = _(scientificData.value).filter(x => x.parameters.part == 1).orderBy(x => x.parameters.order).value()

  $q.notify({
    message: 'Успешно удалено :(',
    position: 'top-right',
    color: 'info',
  })
}

async function deletePublishData(id) {
  let r = await api.delete(`/api/generator/${id}/del-scientific-work/`)

  const key = _.findKey(scientificData.value, x => x.id == id)
  scientificData.value.splice(key, 1)
  scientificPublishData.value = _(scientificData.value).filter(x => x.parameters.part == 2).orderBy(x => x.parameters.order).value()

  $q.notify({
    message: 'Успешно удалено :(',
    position: 'top-right',
    color: 'info',
  })
}

async function copyPlan() {
  let r = await api.get('/api/generator/')
}

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка данных"})
  await fetchPlanData()
  await fetchHandbook()

  scientificDissertData.value = _(scientificData.value).filter(x => x.parameters.part == 1).orderBy(x => x.parameters.order).value()
  scientificPublishData.value = _(scientificData.value).filter(x => x.parameters.part == 2).orderBy(x => x.parameters.order).value()

  kurs.value = 1
  $q.loading.hide()
})

watch(kurs, () => {
  scientificResearchAutumn.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 1).orderBy(x => x.parameters.order).value()
  scientificResearchWinter.value = _(scientificData.value).filter(x => x.parameters.semester == ((kurs.value - 1) * 2) + 2).orderBy(x => x.parameters.order).value()
}, {immediate: true})

</script>

<template>
  <div class="q-pa-lg q-gutter-y-sm">
    <div class="flex justify-between">
      <q-btn @click="router.push('/scientific-plan')" color="primary" icon="mdi-arrow-left" label="Назад, к списку"/>
      <div class="q-gutter-x-sm">
        <q-btn target="_blank" :href="`${FORCE_SCRIPT_NAME}/api/generator/${mainInfo?.id}/get-scientific-report/`" color="info" icon="mdi-file-document" label="Печать документа"/>
<!--        <q-btn label="Скопировать план" color="primary" icon="mdi-clipboard-outline"/>-->
      </div>
    </div>
    <q-stepper
      v-model="step"
      color="primary"
      animated
      header-nav
    >

      <q-step
        :name="0"
        title="Основная информация"
        icon="mdi-text-box"
        active-icon="mdi-text-box"
      >
        <div class="q-gutter-y-sm q-mb-sm">
          <q-btn @click="showHelpFirstPage = !showHelpFirstPage"
                 :label="showHelpFirstPage ? 'Скрыть подсказку' : 'Открыть подсказку'" color="info"/>
          <q-card class="bg-blue-2" v-if="showHelpFirstPage">
            <q-card-section>
              <p>
                Данный раздел заполняется автоматически, если есть данные которые "подтянулись" у Вас нет возможности
                их исправить.
              </p>
              <p>
                После завершения работы с каждой вкладкой можно переходить к следующей. Все наработки сохранятся и в
                дальнейшем будут выгружены в соответствующий раздел бумажного варианта плана научной деятельности
              </p>
            </q-card-section>
          </q-card>
        </div>

        <q-table
          :columns="columns"
          :rows="rows"
          :rows-per-page-options="[0]"
          hide-header
          hide-bottom
          separator="cell"
        >

<!--          <template #body-cell-val="props">-->
<!--            <q-td :props="props">-->
<!--              {{ props.row.val }}-->
<!--              <q-popup-edit v-slot="scope" v-model="props.row.val" auto-save>-->
<!--                <q-input v-model="scope.value" autofocus @focusout="scope.set" @keyup.enter="scope.set" :debounce="1000"-->
<!--                         @update:modelValue="saveMainInfo(scope.value, props.row.key)"/>-->
<!--              </q-popup-edit>-->
<!--            </q-td>-->
<!--          </template>-->

        </q-table>
      </q-step>

      <q-step
        :name="1"
        title="Примерный план выполнения научного исследования"
        icon="mdi-clipboard-clock-outline"
        active-icon="mdi-clipboard-clock-outline"
      >
        <div class="q-gutter-y-sm q-mb-sm">
          <q-btn @click="showHelpSecondPage = !showHelpSecondPage"
                 :label="showHelpSecondPage ? 'Скрыть подсказку' : 'Открыть подсказку'" color="info"/>
          <q-card class="bg-blue-2" v-if="showHelpSecondPage">
            <q-card-section>
              <div>
                <p>
                  План на каждый семестр должен содержать виды работ, соответствующие логике проведения научного
                  исследования
                  в вашей предметной области. В некоторых семестрах уже имеются предложенные варианты, которые можно
                  оставить
                  без изменения, удалить все либо некоторые или отредактировать. При нажатии на «Добавить вид работ»
                  можно
                  воспользоваться вариантами из выпадающего списка (кнопка «Добавить») или предложить свои варианты,
                  заполнив
                  пустое поле.
                </p>
                <p>
                  После завершения работы с каждой вкладкой можно переходить к следующей. Все наработки сохранятся и в
                  дальнейшем будут выгружены в соответствующий раздел бумажного варианта плана научной деятельности.
                </p>
                <p>
                  Необходимо предложить как можно больше вариаций на каждый семестр, так как определённые Вами виды
                  работ
                  будут использованы аспирантами данной образовательной программы для формирования индивидуального плана
                  работы!
                </p>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <q-stepper v-model="kurs" header-nav animated>
          <q-step
            v-for="kurs in parseInt(mainInfo.rng)"
            :title="`${kurs} курс`"
            :name="kurs"
          >
            <div class="row" style="gap: 4px;">
              <div class="col text-subtitle1">Семестр {{ ((kurs - 1) * 2) + 1 }}</div>
              <div class="col text-subtitle1">Семестр {{ ((kurs - 1) * 2) + 2 }}</div>
            </div>
            <div class="row" style="gap: 4px;">
              <div class="col">
                <draggable
                  :list="scientificResearchAutumn"
                  class="q-gutter-y-sm"
                  handle=".handle"
                  item-key="id"
                  @end="detectMoveAutumn"
                >
                  <template #item="{ element, index }">
                    <div>
                      <q-input v-model="element.text" outlined :debounce="500" @update:modelValue="detectMoveAutumn">
                        <template #append>
                          <q-btn flat color="negative" icon="mdi-delete" @click="deleteWorkScience(element.id)"/>
                          <q-btn flat color="black" icon="mdi-cursor-move" class="handle"/>
                        </template>
                      </q-input>
                    </div>
                  </template>
                </draggable>
                <q-btn class="full-width q-mt-sm" color="primary" label="Добавить вид работ"
                       @click="openAddWorkDialog(((kurs - 1) * 2) + 1, 0)"/>
              </div>
              <div class="col">
                <draggable
                  :list="scientificResearchWinter"
                  class="q-gutter-y-sm"
                  handle=".handle"
                  item-key="id"
                  @end="detectMoveWinter"
                >
                  <template #item="{ element, index }">
                    <div>
                      <q-input v-model="element.text" outlined :debounce="500" @update:modelValue="detectMoveWinter">
                        <template #append>
                          <q-btn flat color="negative" icon="mdi-delete" @click="deleteWorkScience(element.id)"/>
                          <q-btn flat color="black" icon="mdi-cursor-move" class="handle"/>
                        </template>
                      </q-input>
                    </div>
                  </template>
                </draggable>
                <q-btn class="full-width q-mt-sm" color="primary" label="Добавить вид работ"
                       @click="openAddWorkDialog(((kurs - 1) * 2) + 2, 0)"/>
              </div>
            </div>

          </q-step>
        </q-stepper>

      </q-step>

      <q-step
        :name="2"
        title="Примерный план подготовки диссертации"
        icon="mdi-book-education"
        active-icon="mdi-book-education"
      >
        <div class="q-gutter-y-sm q-mb-sm">
          <q-btn @click="showHelpThirdPage = !showHelpThirdPage"
                 :label="showHelpThirdPage ? 'Скрыть подсказку' : 'Открыть подсказку'" color="info"/>
          <q-card class="bg-blue-2" v-if="showHelpThirdPage">
            <q-card-section>
              <div>
                <p>
                  При заполнении данного раздела можно воспользоваться предложенными вариантами (оставить без изменения,
                  удалить все либо некоторые или отредактировать) либо предложить свои, нажав на кнопку «Добавить вид работ».

                </p>
                <p>
                  После завершения работы во вкладке можно переходить к следующей. Все наработки сохранятся и в
                  дальнейшем будут выгружены в соответствующий раздел бумажного варианта плана научной деятельности.
                </p>
                <p>
                  Необходимо предложить как можно больше вариаций для выбора, так как определённые Вами виды работ будут
                  использованы аспирантами данной образовательной программы для формирования индивидуального плана
                  работы!
                </p>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <draggable
          :list="scientificDissertData"
          class="q-gutter-y-sm q-mt-sm"
          handle=".handle"
          item-key="id"
          @end="detectMoveDissert"
        >
          <template #item="{ element, index }">
            <div>
              <q-input v-model="element.text" outlined :debounce="500" @update:modelValue="detectMoveDissert">
                <template #append>
                  <q-btn flat color="negative" icon="mdi-delete" @click="deleteDissertData(element.id)"/>
                  <q-btn flat color="black" icon="mdi-cursor-move" class="handle"/>
                </template>
              </q-input>
            </div>
          </template>
        </draggable>
        <q-btn class="full-width q-mt-sm" color="primary" label="Добавить вид работ"
               @click="addRowDissertData"/>

      </q-step>

      <q-step
        :name="3"
        title="Примерный план подготовки публикаций"
        icon="mdi-clipboard-check-multiple"
        active-icon="mdi-clipboard-check-multiple"
      >
        <div class="q-gutter-y-sm q-mb-sm">
          <q-btn @click="showHelpFourPage = !showHelpFourPage"
                 :label="showHelpFourPage ? 'Скрыть подсказку' : 'Открыть подсказку'" color="info"/>
          <q-card class="bg-blue-2" v-if="showHelpFourPage">
            <q-card-section>
              <div>
                <p>
                  При заполнении данного раздела можно воспользоваться предложенными вариантами (оставить без изменения,
                  удалить все либо некоторые или отредактировать) либо предложить свои, нажав на кнопку «Добавить вид
                  работ».

                </p>
                <p>
                  После завершения работы во вкладке можно переходить к следующей. Все наработки сохранятся и в
                  дальнейшем будут выгружены в соответствующий раздел бумажного варианта плана научной деятельности.
                </p>
                <p>
                  Необходимо предложить как можно больше вариаций для выбора, так как определённые Вами виды работ будут
                  использованы аспирантами данной образовательной программы для формирования индивидуального плана
                  работы!
                </p>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <draggable
          :list="scientificPublishData"
          class="q-gutter-y-sm q-mt-sm"
          handle=".handle"
          item-key="id"
          @end="detectMovePublish"
        >
          <template #item="{ element, index }">
            <div>
              <q-input v-model="element.text" outlined :debounce="500" @update:modelValue="detectMovePublish">
                <template #append>
                  <q-btn flat color="negative" icon="mdi-delete" @click="deletePublishData(element.id)"/>
                  <q-btn flat color="black" icon="mdi-cursor-move" class="handle"/>
                </template>
              </q-input>
            </div>
          </template>
        </draggable>
        <q-btn class="full-width q-mt-sm" color="primary" label="Добавить вид работ"
               @click="addRowPublishData"/>
      </q-step>

    </q-stepper>
  </div>

  <q-dialog v-model="addWorkDialog" persistent>
    <q-card style="width: 700px">
      <q-card-section class="text-subtitle1">
        Добавление работ
      </q-card-section>

      <q-card-section>
        <q-select outlined label="Выберите вид работы" v-model="work" :options="scientificWorks" map-options emit-value
                  option-label="name" option-value="name"/>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Добавить" flat color="positive" @click="addWorkInScience"/>
        <q-btn label="Отмена" flat color="negative" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<style scoped>

</style>
