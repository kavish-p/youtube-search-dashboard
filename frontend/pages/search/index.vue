<template>
    <div class="main-container">
        <el-row>
            <el-col :span="12">
                <el-form :label-position="labelPosition" :rules="rules" label-width="150px" :model="query" ref="query" class="form">
                    <el-form-item label="YouTube Link" size="mini" prop="link">
                        <el-input placeholder="YouTube Link" v-model="query.link" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="Search Terms" size="mini" prop="search_terms">
                        <el-input placeholder="Search Terms (comma-separated)" v-model="query.search_terms" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="Analysis Interval" size="mini" prop="analysis_interval">
                        <el-input placeholder="Analysis Interval (seconds)" v-model.number="query.analysis_interval" type="number" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="Start Time" size="mini" prop="start_time">
                        <el-input placeholder="Start Time (seconds)" v-model.number="query.start_time" type="number" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="End Time" size="mini" prop="end_time">
                        <el-input placeholder="End Time (seconds)" v-model.number="query.end_time" type="number" clearable></el-input>
                    </el-form-item>
                    <el-form-item size="small">
                        <el-button type="primary" icon="el-icon-search" @click="submitForm('query')">Search</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <el-col :span="12">
                <youtube :player-vars="player_vars" :video-id="video_id" @ready="ready"/>
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="9">
                <div class="results">
                    <el-table :data="results" height="500" v-loading="loading">
                        <el-table-column prop="lower_timestamp" label="Lower Timestamp" width="140"></el-table-column>
                        <el-table-column prop="upper_timestamp" label="Upper Timestamp" width="145"></el-table-column>
                        <el-table-column prop="count" label="Count" width="65"></el-table-column>
                        <el-table-column
                        label="Action">
                            <template slot-scope="scope">
                                <el-button type="success" size="mini" @click="showComments(scope.$index, scope.row)">View Matched</el-button>
                                <el-button type="primary" size="mini" @click="showAllComments(scope.$index, scope.row)">View All</el-button>
                                <el-button type="warning" size="mini" @click="seek(scope.$index, scope.row)">Seek</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-col>
            <el-col :span="15">
                <div class="results">
                    <el-table border :data="current_messages" height="500" v-loading="messages_table_loading">
                        <el-table-column prop="time_text" label="Time" width="100"></el-table-column>
                        <el-table-column prop="time_in_seconds" label="Seconds" width="100"></el-table-column>
                        <el-table-column prop="author.name" label="Author" width="180"></el-table-column>
                        <el-table-column prop="message" label="Message"></el-table-column>
                    </el-table>
                </div>
            </el-col>
        </el-row>

    </div>
    
</template>

<script>
export default {
    async fetch() {},
    data() {
        return {
            labelPosition: 'left',
            query: {
                link: '',
                search_terms: 'lol,imao,草',
                analysis_interval: 60,
                start_time: 0,
                end_time: 120000
            },
            results: [],
            current_messages: [],
            loading: false,
            messages_table_loading: false,
            video_id: 'pMsvr55cTZ0',
            player_vars: { autoplay: 1, start: 0 },
            youtube_player: undefined,
            rules: {
                link: [{required: true}],
                search_terms: [{required: true}],
                analysis_interval: [{required: true}, { type: 'number', message: 'please enter a valid integer value'}],
                start_time : [{ type: 'number', message: 'please enter a valid integer value'}],
                end_time : [{ type: 'number', message: 'please enter a valid integer value'}]
            }
        }
    },
    methods: {
        submitForm(formName){
            var re = /v=(.+)/
            this.video_id = re.exec(this.query.link)[1]

            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.loading = true
                    const url = '/'
                    this.$axios.$post(url, this.query).then(response => {
                        this.loading = false
                        this.results = response
                    })
                    .catch(e => {
                        this.loading = false
                        alert(e.response.data.message)
                    })
                } else {
                    // alert('An error occurred. Please check inputs.')
                    return false;
                }
            });
        },
        showComments(index, row){
            this.current_messages = row.matched_messages
        },
        showAllComments(index, row){
            this.current_messages = row.all_messages
        },
        seek(index, row){
            console.log(row);
            const seek_time = row.lower_bound
            console.log(seek_time);
            this.youtube_player.target.seekTo(seek_time)
        },
        ready(event){
            this.youtube_player = event
        }
    }
}
</script>

<style>

.main-container {
    padding-top: 1%;
}

.el-input {
    padding: 5px 0 5px 0;
}

.form {
    padding: 2% 0 0 2%;
    width: 600px;
}

.results {
    padding: 1% 0 0 2%;
    /* width: 500px; */
}

</style>