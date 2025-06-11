<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {computed} from "vue";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  rpdData,
  semestersData,
  lecturesDisciplineWorkHour,
  disciplineThemesById,
  disciplineThemes,
  disabled,
  activeRpdId,
  disciplineWorkHour,
} = storeToRefs(generatorViewStore)

const sem = defineModel('sem')

const props = defineProps({
  data: {
    required: true
  }
});

function getRowColor(id) {
  let number = _.findKey(props.data, x => x.id == id)
  return number % 2 == 0 ? 'bg-grey-1' : 'bg-white'
}

const maxNumberInSemester = computed(() => {
  let data = _.filter(props.data, (x) => x.semester == sem.value)
  return _.max(_.map(data, (x) => x.num))
})

async function fieldUp(item) {
  let dontChange = disciplineWorkHour.value.filter(x => !(x.semester == item.semester && x.type == item.type));

  let currentData = disciplineWorkHour.value.filter(x => x.semester == item.semester && x.type == item.type);
  let newData = currentData.filter(x => x.num < item.num - 1 && x != item).concat(
    [item],
    currentData.filter(x => x.num >= item.num - 1 && x != item),
  ).map((x, index) => ({...x, num: index + 1}))

  disciplineWorkHour.value = dontChange.concat(newData);
  await api.post(`/api/generator/${activeRpdId.value}/set-work-hours-order/`, {
    order: newData.map(x => x.id)
  })
}

async function fieldDown(item) {
  let dontChange = disciplineWorkHour.value.filter(x => !(x.semester == item.semester && x.type == item.type));

  let currentData = disciplineWorkHour.value.filter(x => x.semester == item.semester && x.type == item.type);
  let newData = currentData.filter(x => x.num <= item.num + 1 && x != item).concat(
    [item],
    currentData.filter(x => x.num > item.num + 1 && x != item),
  ).map((x, index) => ({...x, num: index + 1}))

  disciplineWorkHour.value = dontChange.concat(newData);

  await api.post(`/api/generator/${activeRpdId.value}/set-work-hours-order/`, {
    order: newData.map(x => x.id)
  })
}

const emit = defineEmits(['delete', 'edit'])
</script>

<template>
  <q-tab-panels
    v-model="sem"
    animated
    transition-prev="scale"
    transition-next="scale"
  >
    <q-tab-panel v-for="item in [...semestersData, {num: -1}]" :name="item.num" class="lectures-container">
      <div v-if="item" class="lectures-container__header text-center text-subtitle1 items-center bg-grey-2">
        <div>
          №
        </div>
        <div>
          Название занятия
        </div>
        <div>
          Часов
        </div>
        <div>
          Тема
        </div>
        <div>
          {{ generatorViewStore.semesterYearLabel }}
        </div>
        <div v-show="!disabled">
          Управление
        </div>
      </div>
      <div v-for="lectures in data" class="lectures-container__body">
        <div v-if="sem == -1 || lectures.semester == sem"
             class="lectures-container__body__cell text-subtitle1 text-center items-center"
             :class="getRowColor(lectures.num)">
          <div>
            {{ lectures.num }}
          </div>
          <div>
            {{ lectures.name }}
          </div>
          <div>
            {{ lectures.hours }}
          </div>

          <div>
            {{ disciplineThemesById[lectures.theme_id]?.num }}. {{ disciplineThemesById[lectures.theme_id]?.name }}
          </div>
          <div>
            {{ lectures.semester }}
          </div>
          <div v-show="!disabled">
            <q-btn
              icon="mdi-delete" color="red" flat @click="emit('delete', lectures.id)"
            />
            <q-btn
              icon="mdi-pencil-outline" color="green" flat @click="emit('edit', lectures.id)"
            />
            <q-btn v-if="lectures.num != 1"
                   icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                   @click="fieldUp(lectures)"
            />
            <q-btn v-if="lectures.num != maxNumberInSemester"
                   icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                   @click="fieldDown(lectures)"
            />
          </div>
        </div>
      </div>
    </q-tab-panel>
  </q-tab-panels>
</template>

<style lang="scss" scoped>

.lectures-container {

  $border: solid 1px silver;

  > .lectures-container__header {
    display: grid;
    grid-template-columns: 4% 1fr 15% 25% 10%  20%;
    font-weight: bold;
    border: $border;
    border-bottom: none;

    &:last-child {
      border-bottom: $border;
    }
  }

  > .lectures-container__body {
    > .lectures-container__body__cell {
      display: grid;
      grid-template-columns: 4% 1fr 15% 25% 10%  20%;
      border: $border;
      border-bottom: none;

    }

    &:last-child {
      border-bottom: $border;
    }
  }
}
</style>
