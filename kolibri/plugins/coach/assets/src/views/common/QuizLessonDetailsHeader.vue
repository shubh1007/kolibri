<template>

  <KPageContainer style="padding-top: 24px">
    <BackLink
      :to="backlink"
      :text="backlinkLabel"
    />

    <!-- Cheating to get the same layout effect but not
           using a backlink...
      -->
    <HeaderWithOptions>
      <template #header>
        <div>
          <h1 class="exam-title">
            <!-- KLabeledIcon does not have an 'exam' token, but rather 'quiz' -->
            <KLabeledIcon
              :icon="examOrLesson === 'exam' ? 'quiz' : 'lesson'"
              :label="resource.title"
            />
          </h1>
          <StatusElapsedTime
            v-show="!$isPrint"
            :date="createdDate"
            actionType="created"
          />
        </div>
      </template>
      <template #options>
        <div>
          <slot name="dropdown"></slot>
        </div>
      </template>
    </HeaderWithOptions>
    <MissingResourceAlert v-if="resource.missing_resource" />
  </KPageContainer>

</template>


<script>

  import { mapState } from 'vuex';
  import MissingResourceAlert from 'kolibri-common/components/MissingResourceAlert';
  import HeaderWithOptions from './HeaderWithOptions';
  import StatusElapsedTime from './StatusElapsedTime';
  import BackLink from './BackLink';

  export default {
    name: 'QuizLessonDetailsHeader',
    components: {
      HeaderWithOptions,
      MissingResourceAlert,
      StatusElapsedTime,
      BackLink,
    },
    props: {
      backlink: {
        type: Object,
        required: true,
      },
      backlinkLabel: {
        type: String,
        required: true,
      },
      examOrLesson: {
        type: String,
        required: true,
        validator(value) {
          return ['exam', 'lesson'].includes(value);
        },
      },
    },
    computed: {
      ...mapState('classSummary', ['examMap', 'lessonMap']),
      exam() {
        return this.examMap[this.$route.params.quizId] || {};
      },
      lesson() {
        return this.lessonMap[this.$route.params.lessonId] || {};
      },
      resource() {
        return this.examOrLesson === 'lesson' ? this.lesson : this.exam;
      },
      createdDate() {
        if (this[this.examOrLesson].date_created) {
          return new Date(this[this.examOrLesson].date_created);
        } else {
          return null;
        }
      },
    },
  };

</script>


<style lang="scss" scoped>

  .exam-title {
    margin-bottom: 0;
    font-size: 1.5rem;
  }

  /deep/ .time-context {
    margin-bottom: 0;
  }

</style>
