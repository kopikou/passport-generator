<script setup lang="ts">

import {onBeforeMount, ref, watch, computed} from "vue";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import GeneratorAddLecturesDialog from "pages/generator/components/dialogs/GeneratorAddLecturesDialog.vue";
import _ from "lodash";
import {api} from "boot/axios";
import EmptyIcon from "components/EmptyIcon.vue";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  rpdData,
  semestersData,
  lecturesDisciplineWorkHour,
  disciplineThemes,
} = storeToRefs(generatorViewStore)

const tab = ref(0)

const allPercent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => x.hours)
  return _.sum(value) || 0
})

const allSemesterPercent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.lekc)
  return _.sum(hoursList) || 0
})

const allSemesterPercentValue = computed(() => {
  let value = _.map(lecturesDisciplineWorkHour.value, (x) => x.semester == tab.value ? x.hours : 0)
  return _.sum(value) || 0
})

function addLectures() {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  })
}

function updateLectures(id) {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

function deleteLectures(id) {
  $q.dialog({
    title: 'Удаление темы',
    message: 'Вы точно хотите отправить тему в архив?',
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

const disciplineThemesByValue = computed(() => {
  return _.keyBy(disciplineThemes.value, 'id')
})

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень лекционных работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-if="allPercent != 0">
        <q-btn label="Добавить новую лекционную работу" color="teal" class="q-mb-md" @click="addLectures"/>
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
          <q-tab-panel v-for="item in semestersData" :name="`${item.num}`" class="lectures-container">
            <div v-if="item" class="lectures-container__header text-center text-subtitle1 items-center">
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
            <div v-for="lectures in lecturesDisciplineWorkHour" class="lectures-container__body">
              <div v-if="lectures.semester == tab"
                   class="lectures-container__body__cell text-subtitle1 text-center items-center">
                <div>
                  {{ lectures.name }}
                </div>
                <div>
                  {{ lectures.hours }}
                </div>
                <div>
                  {{ disciplineThemesByValue[lectures.theme_id]?.name }}
                </div>
                <div>
                  <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteLectures(lectures.id)"
                  />
                  <q-btn
                    icon="mdi-update" color="green" flat @click="updateLectures(lectures.id)"
                  />
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </div>
      <div v-else>
        <p class="text-h6">Нет часов по лекционным занятиям</p>
              <empty-icon />
      </div>
    </div>
  </div>
</template>

<style scoped>

.lectures-container {
  > .lectures-container__header {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    font-weight: bold;
  }

  > .lectures-container__body {
    > .lectures-container__body__cell {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
    }
  }
}

</style>
