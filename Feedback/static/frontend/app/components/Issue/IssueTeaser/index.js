import React, {PropTypes, Component} from 'react';
import {DragSource} from 'react-dnd';
import {Link} from 'react-router';

import styles from './style.scss';
import IssueLabel from '../IssueLabel';
import {ItemTypes} from '../../../constants';
import {IssueTypes} from '../../../constants'

const issueSource = {
  canDrag(props) {
    return props.canDrag;
  },

  beginDrag(props) {
    return {
      issue: props,
      onDrop: props.onDrop,
    }
  },

  endDrag(props, monitor) {
    const item = monitor.getItem();
    const dropResult = monitor.getDropResult();
  }
};

@DragSource(ItemTypes.ISSUE, issueSource, (connect, monitor) => ({
  connectDragSource: connect.dragSource(),
  isDragging: monitor.isDragging()
}))
export default class IssueTeaser extends Component {
  static propTypes = {
    connectDragSource: PropTypes.func.isRequired,
    isDragging: PropTypes.bool.isRequired,
    onDrop: PropTypes.func.isRequired,
    id: PropTypes.number.isRequired,
    type: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    isAuthor: PropTypes.bool,
    canDrag: PropTypes.bool,
    upvotes: PropTypes.number,
    comments: PropTypes.number,
    preview: PropTypes.bool
  };

  static defaultProps = {
    isAuthor: false,
    canDrag: false,
    upvotes: 0,
    comments: 0,
    preview: false
  };

  render() {
    const {isDragging, connectDragSource} = this.props;
    let upvote_label = this.props.upvotes == 1 ? "upvote" : "upvotes";
    let comment_label = this.props.comments == 1 ? "comment" : "comments";

    let className = this.props.preview === true ? styles.issueTeaserPreview : styles.issueTeaser;
    if (this.props.type == 'security') {
      className = styles.security;
    } else if (this.props.isAuthor) {
      className = styles.owned;
    }


      return connectDragSource(
      <div>
        <Link
          key={this.props.id}
          to={{
            pathname: `/gsi/feedback/issue/${this.props.id}`,
            state: {returnTo: '/gsi/feedback'}
          }}
          className={className} >
          <IssueLabel type={this.props.type} title={this.props.title} />
          <div className={styles.footer}>
            <span className={styles.upvotes}>
              <i className="fa fa-thumbs-up"></i> {this.props.upvotes} {upvote_label}
            </span>
            <span className={styles.comments}>
              <i className="fa fa-comments"></i> {this.props.comments} {comment_label}
            </span>
          </div>
        </Link>
      </div>
    );
  }
}
