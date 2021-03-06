import React from 'react';
import {Link} from 'react-router';

export default class Modal extends React.Component {
  constructor(props) {
    super(props);

    this.close = this.close.bind(this);
  }

  render() {
    return (
      <div className="modal" onClick={this.close}>
        <div className="modal__window" onClick={this.eventHandler}>
          <div className="modal__header">
            <Link to={this.props.returnTo}>
              <button className="modal__close">
                <i className="fa fa-times-circle"></i>
              </button>
            </Link>
          </div>
          <div>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }

  close(event) {
    this.props.onClose();
  }

  eventHandler(event) {
    event.stopPropagation();
  }
}
