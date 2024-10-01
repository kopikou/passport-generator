<script setup lang="ts">

import {computed, onBeforeMount, ref, watch} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddPracticeDialog from "pages/generator/components/dialogs/GeneratorAddPracticeDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  practiceDisciplineWorkHour,
  rpdData,
  disciplineThemes,
} = storeToRefs(generatorViewStore)
const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.pr)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(practiceDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.pr)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(practiceDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addPractice() {
  $q.dialog({
    component: GeneratorAddPracticeDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  })
}

function updatePractice(id) {
  $q.dialog({
    component: GeneratorAddPracticeDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

function deletePractice(id) {
  $q.dialog({
    title: 'Удаление практического занятия',
    message: 'Вы точно хотите отправить практическое занятие в архив?',
    ok: {
      label: 'В архив',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {

    $q.loading.show({message: "Удаление"})
    let r = await api.get('/api/generator/delete-discipline-work-hour/', {params: {id: id}})

    rpdData.value.discipline_work_hour.splice(_.findKey(rpdData.value.discipline_work_hour, (x) => x.id == id), 1)

    $q.loading.hide()
  })
}

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень практических работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-if="allPercent != 0">
        <q-btn label="Добавить новую практическую рработу" color="teal" class="q-mb-md" @click="addPractice"/>
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allPercentValue / allPercent" color="teal">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black" :label="`${allPercentValue} / ${allPercent}`"/>
          </div>
        </q-linear-progress>
        <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
        >
          <q-tab class="text-teal bg-grey-4" v-for="item in semestersData" :name="`${item.num}`"
                 :label="`${item.num}`"/>
        </q-tabs>
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allSemesterPercentValue / allSemesterPercent"
                           color="primary">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black" :label="`${allSemesterPercentValue} / ${allSemesterPercent}`"/>
          </div>
        </q-linear-progress>
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
        >
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="practice-container">
            <div v-if="item" class="practice-container__header text-center text-subtitle1 items-center">
              <div>
                Наименование раздела
              </div>
              <div>
                Количество часов
              </div>
              <div>
                Тема дисциплины
              </div>
              <div>
                Управление
              </div>
            </div>
            <div v-for="practice in practiceDisciplineWorkHour" class="practice-container__body">
              <div v-if="practice.semester == tab"
                   class="practice-container__body__cell text-subtitle1 text-center items-center">
                <div>
                  {{ practice.name }}
                </div>
                <div>
                  {{ practice.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[practice.theme_id]?.name }}
                </div>
                <div>
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deletePractice(practice.id)"
                  />
                  <q-btn
                    icon="mdi-update" color="green" flat @click="updatePractice(practice.id)"
                  />
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </div>
      <div v-else>
        <p class="text-h6">Нет часов по практическим занятиям</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.practice-container {
  > .practice-container__header {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    font-weight: bold;
  }

  > .practice-container__body {
    > .practice-container__body__cell {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
    }
  }
}
</style>
